FROM python:3.12-slim-bookworm

EXPOSE 8501

RUN apt-get update && apt-get install -y \
    build-essential \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt setup.py pyproject.toml ./
COPY Recomendation_System/__init__.py Recomendation_System/__init__.py
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . /app

ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]