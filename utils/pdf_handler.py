from pypdf import PdfReader

from langchain_text_splitters import RecursiveCharacterTextSplitter


def get_pdf_text(uploaded_files):
    """
    Extracts text from all pages of uploaded PDF files.
    Adds file name and page number markers for source citation.

    Example:
    - File: "model3_manual.pdf", Page 1: "续航里程 606km"
    - Result: "[文档: model3_manual.pdf | 第1页] 续航里程 606km"
    """
    text = ""
    for file in uploaded_files:
        reader = PdfReader(file)
        file_name = file.name
        for i, page in enumerate(reader.pages):
            page_text = page.extract_text() or ""
            if page_text.strip():
                # Mark each page with file name and page number for retrieval traceability
                text += f"\n[文档: {file_name} | 第{i+1}页]\n{page_text}\n"
    return text


def get_text_chunks(text):
    """
    Splits large text into overlapping chunks optimized for Chinese documents.

    Key differences from the original English version:
    - chunk_size: 5000 → 300 (Chinese info density is much higher per character)
    - chunk_overlap: 500 → 50  (lower redundancy needed with smaller chunks)
    - Added Chinese punctuation separators (。, ，) for semantic boundary awareness

    Example:
    If a car manual section reads "续航606km。快充30分钟可达80%。",
    the splitter will prefer to cut at "。" rather than mid-sentence.
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=300,          # Optimized for Chinese: ~200-300 tokens per chunk
        chunk_overlap=50,        # Moderate overlap to reduce noise
        separators=[             # Chinese-friendly split priority
            "\n\n",              # 1st: paragraph breaks
            "\n",                # 2nd: line breaks
            "。",                # 3rd: Chinese period
            "，",                # 4th: Chinese comma
            ". ",                # 5th: English period + space
            " ",                 # 6th: spaces
            ""                   # 7th: character-level (last resort)
        ]
    )
    return splitter.split_text(text)
