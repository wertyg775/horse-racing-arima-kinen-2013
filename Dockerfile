# 1️⃣ Base image: use Python 3.13
FROM python:3.11-slim

# 2️⃣ Environment variables for clean output
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 3️⃣ Set working directory inside the container
WORKDIR /app

# 4️⃣ Copy only requirements first (for caching)
COPY requirements_backup.txt /app/requirements.txt

# 5️⃣ Install system dependencies + Python dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip && pip install -r /app/requirements.txt

RUN pip install --no-cache-dir -r /app/requirements.txt


# 6️⃣ Copy the rest of your code
COPY . /app

# 7️⃣ Expose Streamlit’s default port
EXPOSE 8501

# 8️⃣ Run Streamlit (your app is inside /app/src)
CMD ["streamlit", "run", "src/app.py", "--server.port=8501", "--server.address=0.0.0.0"]
