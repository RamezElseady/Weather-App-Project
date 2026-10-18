# 🌤️ End-to-End Weather Forecasting App (DevOps & Observability Pipeline)

A production-ready DevOps project showcasing a Python (Flask) Weather Forecasting Application built with a modern Glassmorphism UI, containerized with Docker, automatically deployed via GitLab CI/CD to AWS EC2, and fully monitored using Prometheus and Grafana.

---

## 🏗️ Architecture & System Workflow 

```
[ Developer ] ➔ Push Code ➔ [ GitLab CI/CD Pipeline ]
                                      │
                                      ▼
                        [ GitLab Container Registry ]
                                      │
                                      ▼
                                [ AWS EC2 ]
                   ┌──────────────────┴──────────────────┐
                   ▼                                     ▼
          [ Docker Containers ]              [ Observability Stack ]
          • Weather App (:5000) ───────┐ ──► [ Prometheus (:9090) ]
          • Node Exporter (:9100) ─────┘             │
                                                     ▼
                                            [ Grafana (:3000) ]
```

---

## 🛠️ Tech Stack

* **Application:** Python 3.10, Flask, Bootstrap 5 (Glassmorphism UI), WeatherAPI / RapidAPI
* **Containerization:** Docker
* **CI/CD Pipeline:** GitLab CI/CD, GitLab Container Registry
* **Cloud Infrastructure:** AWS EC2 (Ubuntu Linux)
* **Monitoring & Observability:** Prometheus, Grafana, Node Exporter

---

## ✨ Key Features & Technical Highlights

* **Interactive Frontend:** Dynamic weather queries with seamless API integration.
* **Automated CI/CD Pipeline:** Fully automated build and SSH deployment workflow on pushes to `main`.
* **Custom Metric Instrumentation:** Exposing application metrics via `/metrics` (`weather_app_requests_total`).
* **Full-Stack Observability:** 
  * Infrastructure metrics (CPU, RAM, Disk, Network) via **Node Exporter**.
  * Dynamic real-time application metrics tracked via **Prometheus**.
  * Customized **Grafana Dashboards** for unified visualization.

---

## 🚀 Local Setup & Run Guide

### 1. Clone Repository
```bash
git clone <YOUR_GITLAB_REPO_URL>
cd weather-forecasting-app
```

### 2. Set Environment Variables
```bash
export RAPIDAPI_KEY="your_rapidapi_key_here"
```

### 3. Run with Docker
```bash
docker build -t weather-app .
docker run -d -p 5000:5000 -e RAPIDAPI_KEY=$RAPIDAPI_KEY weather-app
```

---

## 📊 Observability Configuration

### Prometheus Scraping Configuration (`prometheus.yml`)
```yaml
global:
  scrape_interval: 5s

scrape_configs:
  - job_name: 'weather-app'
    static_configs:
      - targets: ['<EC2_PUBLIC_IP>:5000']

  - job_name: 'ec2-server'
    static_configs:
      - targets: ['<EC2_PUBLIC_IP>:9100']
```

---

## 📸 Monitoring Dashboards

* **Prometheus Endpoint:** `http://<EC2_PUBLIC_IP>:9090`
* **Grafana Dashboard:** `http://<EC2_PUBLIC_IP>:3000`