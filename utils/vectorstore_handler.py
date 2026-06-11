import os

from utils.config import (
    GOOGLE_API_KEY, MODEL_OPTIONS, CHINESE_EMBEDDING_MODEL
)
from utils.pdf_handler import get_pdf_text, get_text_chunks

from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings

# Mapping each model provider to its corresponding persistent directory
PERSIST_DIR = {
  key.lower(): f"./data/{key.lower()}_vector_store.chroma"
  for key in MODEL_OPTIONS.keys()
}


def get_embeddings(model_provider):
    """
    Returns the appropriate embedding model based on the selected provider.

    🔑 KEY CHANGE: All providers now use a Chinese-optimized embedding model
    (shibing624/text2vec-base-chinese) instead of English MiniLM.
    This dramatically improves Chinese semantic retrieval accuracy.

    For Gemini, we keep Google's embedding service as an alternative
    since it has good multilingual support.
    """
    USE_CHINESE_EMBEDDING = True  # Toggle for A/B comparison experiments

    if USE_CHINESE_EMBEDDING:
        # Local, CPU-only, ~400MB model file. No API key needed.
        # Specialized for Chinese semantic similarity.
        return HuggingFaceEmbeddings(model_name=CHINESE_EMBEDDING_MODEL)

    if model_provider == "groq":
        return HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L12-v2"
        )
    elif model_provider == "gemini":
        return GoogleGenerativeAIEmbeddings(
            model="models/embedding-001",
            google_api_key=GOOGLE_API_KEY
        )
    elif model_provider == "deepseek":
        # DeepSeek doesn't offer an embedding API, fall back to Chinese local model
        return HuggingFaceEmbeddings(model_name=CHINESE_EMBEDDING_MODEL)
    elif model_provider == "ollama (local)":
        from langchain_ollama import OllamaEmbeddings
        return OllamaEmbeddings(model="nomic-embed-text")
    else:
        raise ValueError(f"Unsupported Model Provider: {model_provider}")


def get_or_create_vectorstore(uploaded_files, model_provider):
    """
    Loads an existing Chroma vectorstore from disk, or creates a new one
    from uploaded PDFs.

    Workflow:
    1. Extract raw text from uploaded PDFs (with page markers)
    2. Split text into Chinese-optimized chunks
    3. Embed chunks using Chinese embedding model
    4. Persist to ChromaDB on disk

    Args:
        uploaded_files (list): List of uploaded PDF files.
        model_provider (str): Lowercase name of the selected provider.

    Returns:
        Chroma: A Chroma vectorstore containing embedded PDF text chunks.
    """
    # Extract raw text from the uploaded PDF files
    raw_text = get_pdf_text(uploaded_files)

    # Chunk the raw text for embedding
    chunks = get_text_chunks(raw_text)

    print(f"[PDF] 提取文本: {len(raw_text)} 字符 -> 分割为 {len(chunks)} 个文本块")

    # Load the appropriate embedding model
    embedding = get_embeddings(model_provider)

    # Define directory path to store or retrieve Chroma DB
    persist_path = PERSIST_DIR.get(
        model_provider,
        f"./data/{model_provider}_vector_store.chroma"
    )

    # If the vectorstore directory exists and is not empty, load and append
    if os.path.exists(persist_path) and os.listdir(persist_path):
        print(f"[DB] 加载已有向量库: {persist_path}")
        vectorstore = Chroma(
            persist_directory=persist_path,
            embedding_function=embedding
        )
        vectorstore.add_texts(chunks)
    else:
        print(f"[DB] 创建新向量库: {persist_path}")
        vectorstore = Chroma.from_texts(
            texts=chunks,
            embedding=embedding,
            persist_directory=persist_path
        )

    return vectorstore
