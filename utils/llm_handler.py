from utils.config import (
    GOOGLE_API_KEY, GROQ_API_KEY, DEEPSEEK_API_KEY
)

from langchain_core.prompts import ChatPromptTemplate
from langchain_classic.chains import create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI


# =====================================================================
#  🚗 汽车产品手册智能问答 — 专用 Prompt 模板
# =====================================================================
#  This is the key "AI application design" work — translating a business
#  scenario (car manual Q&A) into an AI solution (custom RAG prompt).
#  The 6 rules below constrain the LLM to behave as a professional
#  automotive product advisor with source citation.

CAR_MANUAL_SYSTEM_PROMPT = """你是一个专业的新能源汽车产品顾问，你的所有知识来源于用户上传的车型产品手册。

请严格遵守以下规则：
1. 只根据下方提供的文档内容回答问题，禁止使用你的训练数据
2. 回答时标注信息来源，格式：[文档名，第X页]
3. 如果文档中没有相关信息，直接说"本手册中未提及此信息"，不要猜测
4. 如果用户比较不同车型，请客观对比文档中的数据，不要偏向任何一个品牌
5. 优先给出具体数字和参数，用简洁清晰的中文回答
6. 如果用户的问题有歧义（如"电池能用多久"可能指续航里程或电池寿命），先用一句话澄清你的理解，再回答"""

CAR_MANUAL_USER_PROMPT = """以下是产品手册的相关段落：

{context}

用户的问题是：{input}

请根据以上文档内容回答。如有数据，请引用具体数值和来源页码。"""

# =====================================================================


def get_llm_chain(model_provider, model, vectorstore):
    """
    Builds and returns a LangChain RAG (Retrieval-Augmented Generation) chain.

    🔑 KEY CHANGES from original:
    1. Added DeepSeek support (langchain-openai compatible base_url)
    2. Replaced generic English prompt with car-manual-specific Chinese prompt
    3. Added source citation requirement in system prompt
    4. Set temperature=0 for reproducible, factual answers
    5. Increased retrieval k from 3 → 5 for better recall

    Parameters:
    - model_provider (str): "deepseek", "groq", "gemini", or "ollama (local)"
    - model (str): Specific model name
    - vectorstore (VectorStore): Chroma vectorstore for document retrieval

    Returns:
    - A LangChain retrieval chain object
    """
    # Build car-manual-specific prompt template
    prompt = ChatPromptTemplate.from_messages([
        ("system", CAR_MANUAL_SYSTEM_PROMPT),
        ("human", CAR_MANUAL_USER_PROMPT)
    ])

    if not model:
        return None

    # Initialize LLM instance based on provider
    if model_provider == "deepseek":
        # DeepSeek is OpenAI-API-compatible, use ChatOpenAI with custom base_url
        llm = ChatOpenAI(
            model=model,
            api_key=DEEPSEEK_API_KEY,
            base_url="https://api.deepseek.com",
            temperature=0,          # Deterministic output for reliable Q&A
            max_tokens=1024
        )
    elif model_provider == "groq":
        llm = ChatGroq(
            model=model,
            api_key=GROQ_API_KEY,
            temperature=0,
            max_tokens=1024
        )
    elif model_provider == "gemini":
        llm = ChatGoogleGenerativeAI(
            model=model,
            api_key=GOOGLE_API_KEY,
            temperature=0,
            max_output_tokens=1024
        )
    elif model_provider == "ollama (local)":
        from langchain_ollama import ChatOllama
        llm = ChatOllama(
            model=model,
            temperature=0
        )
    else:
        return None

    # Convert vectorstore into a retriever (k=5 for better recall)
    retriever = vectorstore.as_retriever(search_kwargs={"k": 5})

    # Build the full RAG chain: retrieval → prompt stuffing → LLM generation
    chain = create_retrieval_chain(
        retriever,
        create_stuff_documents_chain(llm, prompt=prompt)
    )

    return chain
