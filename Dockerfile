# ============================================
#  RAG PDFBot — Docker 镜像定义
# ============================================
#  用法: docker build -t rag-bot-chroma .
#  运行: docker run -p 8501:8501 --env-file .env rag-bot-chroma
# ============================================

# 1. 基础镜像：Python 3.11 轻量版
FROM python:3.11-slim

# 2. 设置工作目录（容器内的 /app）
WORKDIR /app

# 3. 先复制依赖文件，利用 Docker 缓存加速构建
#    只要 requirements.txt 不变，这一层就不会重新执行
COPY requirements.txt .

# 4. 安装依赖
#    --no-cache-dir: 不缓存 pip 下载，减小镜像体积
RUN pip install --no-cache-dir -r requirements.txt

# 5. 复制项目代码到容器
COPY . .

# 6. 暴露 Streamlit 默认端口
EXPOSE 8501

# 7. 启动命令
#    --server.address=0.0.0.0: 允许外部访问（不只是 localhost）
#    --server.headless=true: 无浏览器模式（服务器环境）
CMD ["streamlit", "run", "app.py", "--server.address=0.0.0.0", "--server.headless=true"]
