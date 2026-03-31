<div align="center">
  
#  BiblioEngine: Book Recommendation System

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![Streamlit App](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat&logo=Streamlit&logoColor=white)](https://streamlit.io/)
[![Dockerized](https://img.shields.io/badge/Docker-2496ED?style=flat&logo=Docker&logoColor=white)](https://www.docker.com/)
[![AWS EC2](https://img.shields.io/badge/Deployed_on-AWS_EC2-FF9900?style=flat&logo=amazon-aws&logoColor=white)](https://aws.amazon.com/ec2/)
[![Scikit-Learn](https://img.shields.io/badge/Machine_Learning-Scikit_Learn-F7931E?style=flat&logo=scikit-learn&logoColor=white)](https://scikit-learn.org/)

*An end-to-end, dynamic collaborative-filtering recommendation system designed to surface highly tailored book suggestions with sub-second latency.*

---
</div>

##  System Overview

**BiblioEngine** is a production-grade machine learning pipeline that powers personalized book discovery. Built around user-item affinity, it leverages [Collaborative Filtering](https://en.wikipedia.org/wiki/Collaborative_filtering) to compute book similarities using K-Nearest Neighbors (KNN). 

The application is structured into a modular pipeline—from raw data ingestion to transformation, model training, and a responsive web interface. It is packaged with Docker for seamless portability and designed for deployment on highly available cloud compute instances (AWS EC2).

##  Key Features

- **Automated Data Pipelines:** Modular architecture handling Data Ingestion, Data Validation, and Data Transformation.
- **Collaborative Filtering Engine:** Unsupervised KNN model running on optimized sparse user-item interaction matrices.
- **MAANG-Grade UI:** A sleek, fully responsive, dark-mode Streamlit interface optimized for user experience (complete with custom CSS, glassmorphism design, and Google Material Icons).
- **Automated Artifact Management:** Models, data states, and encodings are dynamically serialized and versioned locally within `/artifacts`.
- **Production-Ready:** Containerized via Docker (`python:3.12-slim`) with explicitly pinned dependencies.

##  Architecture

The system operates via a configuration-driven pipeline designed for high cohesion and low coupling:

```text
Data Source ──► Configuration Manager ──► Custom Logger / Exception Handler
                      │
               ┌──────▼──────┐
               │  Ingestion  │ (Downloads & extracts zip files)
               └──────┬──────┘
               ┌──────▼──────┐
               │ Validation  │ (Sanitizes features, checks schema)
               └──────┬──────┘
               ┌──────▼──────┐
               │ Transform   │ (Generates pivot tables, sparse matrices)
               └──────┬──────┘
               ┌──────▼──────┐
               │  Trainer    │ (Trains NearestNeighbors model, serializes objects)
               └──────┬──────┘
               ┌──────▼──────┐
               │ Application │ (Streamlit UI loads artifacts & inference engine)
               └─────────────┘
```

##  Technology Stack

| Category | Tools & Frameworks |
| --- | --- |
| **Backend / ML** | Python (3.12), Pandas, NumPy, Scipy, Scikit-Learn |
| **Frontend / UI**   | Streamlit, Custom CSS, Google Material Symbols |
| **DevOps / Infra** | Docker, AWS EC2, Git, GitHub Actions (ready) |
| **Configuration**   | YAML (`config.yaml`), Data Classes |

---

##  Getting Started (Local Development)

### 1. Prerequisites
- Python `3.10` or higher
- Git

### 2. Installation
Clone the repository and spin up an isolated virtual environment:

```bash
git clone https://github.com/chandan1708/BiblioEngine-a-Recomendation-System.git
cd BiblioEngine-a-Recomendation-System

# Create & activate virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Launching the App
Start the Streamlit server. The web UI will be accessible at `http://localhost:8501`.

```bash
streamlit run app.py
```
*(Note: If it's your first run, use the **Admin Sidebar** to trigger the model training pipeline before searching for books).*

---

##  Docker Deployment

The application includes a highly optimized `.dockerignore` and multi-stage-ready `Dockerfile` to guarantee isolated execution.

### Build the Image
```bash
docker build --no-cache -t biblioengine:latest .
```

### Run the Container
```bash
docker run -d -p 8501:8501 --name biblioengine_app biblioengine:latest
```

---

##  AWS EC2 Deployment Guide

1. Provision an **Ubuntu** EC2 instance and open port `8501` in your Security Group.
2. SSH into your instance and install Docker:
   ```bash
   sudo apt-get update -y && sudo apt-get upgrade -y
   curl -fsSL https://get.docker.com -o get-docker.sh
   sudo sh get-docker.sh
   sudo usermod -aG docker ubuntu
   newgrp docker
   ```
3. Clone the repo and run it:
   ```bash
   git clone https://github.com/chandan1708/BiblioEngine-a-Recomendation-System.git
   cd BiblioEngine-a-Recomendation-System
   docker build -t biblioengine:latest .
   docker run -d -p 8501:8501 biblioengine:latest
   ```
4. Access the live app via your EC2 Public IP: <a href="http://13.217.111.62:8501/">http://13.217.111.62:8501/</a></p>

---
<div align="center">
  <p>Built with  by <a href="https://github.com/chandan1708">Chandan R</a></p>
</div>
