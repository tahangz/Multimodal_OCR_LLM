FROM python:3.11-slim

LABEL maintainer="Taha <tahanaguezz@gmail.com>"
LABEL description="Streamlit app for multimodal document summarisation using OCR and Gemini 2.5 Flash."

# Install system dependencies: Tesseract OCR and poppler (for pdf2image)
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    tesseract-ocr \
    poppler-utils \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app/ ./app/

# Expose the Streamlit port
EXPOSE 8501

# Command to run the Streamlit app
CMD ["streamlit", "run", "app/main.py", "--server.port", "8501", "--server.address", "0.0.0.0"]