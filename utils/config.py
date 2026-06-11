import os

from dotenv import load_dotenv

# Load environment variables from .env file into os.environ
load_dotenv()

# API keys for different LLM providers
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")

# Chinese embedding model — specialized for Chinese semantic matching
CHINESE_EMBEDDING_MODEL = "shibing624/text2vec-base-chinese"

# Dictionary of available model providers and their respective models
MODEL_OPTIONS = {
  "DeepSeek": {
    "playground": "https://platform.deepseek.com",
    "models": [
      "deepseek-chat",       # DeepSeek-V3 — all-purpose, great Chinese
      "deepseek-reasoner"    # DeepSeek-R1 — stronger reasoning
    ]
  },
  "Groq": {
    "playground": "https://console.groq.com/",
    "models": [
      "llama-3.1-8b-instant",
      "llama3-70b-8192",
      "qwen-qwq-32b"
    ]
  },
  "Gemini": {
    "playground": "https://ai.google.dev",
    "models": ["gemini-2.0-flash", "gemini-2.5-flash"]
  },
  "Ollama (Local)": {
    "playground": "https://ollama.com",
    "models": ["qwen2.5:7b", "qwen2.5:14b", "llama3.1:8b"]
  }
}
