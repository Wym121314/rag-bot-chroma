# 👽 RAG PDFBot - Modular Edition

This project is a **production-style, modular rebuild** of [rag-bot-basic](https://github.com/Zlash65/rag-bot-basic) — a Retrieval-Augmented Generation (RAG) chatbot that lets you upload and chat with multiple PDFs.

> **What’s different in this version?**
> We’ve restructured everything to reflect how you'd build a scalable real-world RAG app. The UI and logic remain familiar, but the under-the-hood design is completely revamped.

---

## 🔄 What Changed from `rag-bot-basic`

| Area | Old Project | This Project |
|------|-------------|--------------|
| **Modularity** | All logic in a single file | ✅ Split into logical modules: `chat`, `sidebar`, `vectorstore`, `llm`, `pdf_handler`, etc. |
| **PDF Parsing** | `PyPDF2` | ✅ Switched to `pypdf` (more modern & maintained) |
| **Chain Logic** | `load_qa_chain` | ✅ Now uses `RetrievalChain` with `stuff_documents_chain` |
| **Vector Store** | FAISS | ✅ Now uses ChromaDB (with inspection support) |
| **Component Rendering** | Conditional rendering | ✅ All components rendered but disabled until their dependencies are met |
| **Prompt Design** | Static QA prompt | ✅ Custom LangChain prompt template with system/human roles |
| **UI Features** | Same core UI | ✅ Added live vectorstore inspector for developers (`developer_mode.py`) |
| **Error Handling** | Minimal | ✅ Improved error handling and edge case feedback |

---

## 🧪 How It Looks

### Demo

![demo-gif](/assets/rag-bot-chroma.gif)

### UI

![ui-screenshot](/assets/screenshot-5.png)

---

## 🏗️ Architecture

![architecture](/assets/rag-bot-chroma-architecture.png)

---

## 🚀 Features

- 🔌 **Choose Groq or Gemini LLMs**
- 📚 **Upload multiple PDFs**
- 💬 **Chat interface powered by LangChain retrieval chains**
- 🧠 **Contextual embeddings with HuggingFace or Google models**
- 🧹 **Utilities panel: Reset, Clear, Undo**
- 📥 **Downloadable chat history**
- 🧪 **ChromaDB Developer Mode for inspecting embeddings**

---

<details>
  <summary>🛠️ Tech Stack</summary>

- **UI**: Streamlit
- **LLMs**: Groq & Gemini via LangChain
- **Vector DB**: ChromaDB (was FAISS in old version)
- **Embeddings**: HuggingFace & Google GenAI
- **PDF Parsing**: PyPDF
- **Orchestration**: LangChain Retrieval Chain

</details>

---

## 📦 Installation

```bash
git clone https://github.com/Zlash65/rag-bot-chroma.git
cd rag-bot-chroma

python3 -m venv venv
source venv/bin/activate

pip3 install -r requirements.txt
```

---

## 🐳 Docker (一键部署)

```bash
# 1. 先创建 .env 文件（见下方 API Keys 部分）
# 2. 一键启动
docker-compose up --build

# 3. 浏览器打开 http://localhost:8501
```

停止服务：`docker-compose down`

---

## 🔐 API Keys Required

- **Groq API key** from [console.groq.com](https://console.groq.com/)
- **Google Gemini API key** from [ai.google.dev](https://ai.google.dev/)

Create a `.env` file:

```env
GROQ_API_KEY=your-groq-key
GOOGLE_API_KEY=your-google-key
```

---

## ▶️ How to Use

```bash
streamlit run app.py
```

1. Choose your **model provider** (Groq or Gemini)
2. Pick a **model**
3. Upload **PDFs**
4. Click **Submit**
5. Ask anything!

---

<details>
  <summary>📁 Project Structure</summary>

```
.
├── app.py                        # Main app logic
├── Dockerfile                    # Docker image definition
├── docker-compose.yml            # One-click deployment
├── .dockerignore                 # Docker build exclusions
├── utils/
│   ├── chat_handler.py          # Handles chat, input, history, downloads
│   ├── sidebar_handler.py       # Handles sidebar config, upload, utilities
│   ├── llm_handler.py           # LLM and chain setup
│   ├── vectorstore_handler.py   # Embedding + Chroma vectorstore logic
│   ├── pdf_handler.py           # PDF parsing and chunking
│   ├── config.py                # API keys and model metadata
│   └── developer_mode.py        # Inspector for vectorstore queries
├── data/                        # Local vectorstore (Chroma) (not committed)
├── assets/                      # GIFs and images for README
├── .env                         # API keys (not committed)
└── requirements.txt
```
</details>

---

## 🧼 Tools Panel

| Button | Function |
|----------|--------|
| 🔄 Reset | Clears session state and reruns app |
| 🧹 Clear Chat | Clears chat + PDF submission |
| ↩️ Undo | Removes last question/response |

---

## 📦 Download Chat History

Chat history is saved in the session state and can be exported as a CSV with the following columns:

| Question | Answer | Model Provider | Model Name | PDF File | Timestamp |
|----------|--------|----------------|------------|---------------------|-----------|
| What is this PDF about? | This PDF explains... | Groq | llama3-70b-8192 | file1.pdf, file2.pdf | 2025-07-03 21:00:00 |

---

## 🙏 Acknowledgements

- [LangChain](https://www.langchain.com/)
- [Streamlit](https://streamlit.io/)
- [Groq](https://console.groq.com/)
- [Google Gemini](https://ai.google.dev/)
- [Chroma](https://docs.trychroma.com/)

---

## 🧠 Looking for the simpler version?

Check out the original repo here:  
👉 [rag-bot-basic](https://github.com/Zlash65/rag-bot-basic)

Great for understanding the fundamentals before jumping into modularization.
