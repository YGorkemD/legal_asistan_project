# === Base Image ===
FROM python:3.11-slim

# === Set Environment Variables ===
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# === Set Working Directory ===
WORKDIR /app

# === Copy Requirements and Install Dependencies ===
COPY requirements.txt /app/requirements.txt
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# === Copy Project Files ===
COPY src /app/src
COPY data /app/data
COPY models /app/models
COPY configs /app/configs
COPY .env /app/.env

# === Expose Streamlit Port ===
EXPOSE 8501

# === Run Application ===
CMD ["streamlit", "run", "src/app.py", "--server.port=8501", "--server.address=0.0.0.0"]
