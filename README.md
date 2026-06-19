🚨Real-Time Fraud Detection Platform
An end-to-end, event-driven Machine Learning platform that detects fraudulent financial transactions in real time using streaming architectures, online feature stores, and Transformer-based sequence models.
This project simulates a production-grade fraud detection system used by large financial institutions, combining Kafka, Redis, FastAPI, MLflow, Docker, and Transformer models to process and score transactions with low-latency inference.
 
🎯 Project Objective
Build a scalable fraud detection platform capable of:
•	Processing streaming transaction data in real time
•	Maintaining customer behavioral history
•	Detecting anomalous transaction patterns
•	Generating fraud risk scores with low latency
•	Publishing high-risk alerts for downstream systems
•	Supporting deployment-ready ML services
 
🏗️ System Architecture
                    ┌──────────────────────┐
                    │ Transaction Producer │
                    │  (Synthetic Data)    │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │        Kafka         │
                    │   transactions topic │
                    └──────────┬───────────┘
                               │
                               ▼
               ┌────────────────────────────┐
               │ Fraud Scoring Service      │
               │                            │
               │ 1. Retrieve history        │
               │ 2. Build sequences         │
               │ 3. Score transaction       │
               │ 4. Publish alerts          │
               └──────┬──────────┬──────────┘
                      │          │
                      │          │
                      ▼          ▼
              ┌─────────────┐  ┌────────────────┐
              │    Redis    │  │ Rule Engine    │
              │ FeatureStore│  │ (<20 history)  │
              └─────────────┘  └────────────────┘
                      │
                      ▼
            ┌─────────────────────┐
            │  TabTransformer     │
            │ (>=20 transactions) │
            └──────────┬──────────┘
                       │
                       ▼
            ┌─────────────────────┐
            │ Kafka fraud_alerts  │
            └──────────┬──────────┘
                       │
                       ▼
            ┌─────────────────────┐
            │   Alert Service     │
            └─────────────────────┘


---------------------------------------

FastAPI → Docker → AWS Deployment
 
🧠 Machine Learning Approach
Rule Engine (Cold Start)
Used when insufficient customer history is available.
Conditions include:
•	High transaction amounts
•	Foreign country transactions
•	New device usage
•	Merchant anomalies
 
TabTransformer
A Transformer-based sequence model trained on the latest customer transactions.
Input
20 most recent transactions.
Features:
Numerical
•	amount
Categorical
•	merchant
•	country
•	device
•	email_domain
Output
Fraud probability score (0-1).
 
⚙️ Technology Stack
Data Streaming
•	Apache Kafka
Feature Store
•	Redis
Machine Learning
•	PyTorch
•	TabTransformer
•	Rule-Based Engine
MLOps
•	MLflow
•	Docker
APIs
•	FastAPI
Cloud
•	AWS
•	Amazon ECR
•	Amazon ECS Fargate
•	Amazon Sagemaker
Development
•	Python 3.10
•	Docker Desktop
 
📂 Project Structure
fraud-detection-platform/

src/

├── api/

│   └── inference_api.py

├── feature_store/

│   └── redis_history_store.py

├── kafka/

├── models/

│   └── tab_transformer/

│       ├── model.py

│       ├── trainer.py

│       └── predictor.py

├── services/

│   ├── transaction_service/

│   │   ├── producer.py

│   │   ├── customer_profile_generator.py

│   │   └── transaction_generator.py

│   ├── fraud_scoring_service/

│   │   ├── fraud_scoring_service.py

│   │   └── rule_based_scorer.py

│   └── alert_service/

│       └── alert_service.py

config/

models/

Dockerfile

README.md
 
🚀 Running the Platform
Start Kafka
docker compose up -d kafka
Start Producer
python -m src.services.transaction_service.producer
Start Fraud Scoring Service
python -m src.services.fraud_scoring_service.fraud_scoring_service
Start Alert Service
python -m src.services.alert_service.alert_service
Start FastAPI
uvicorn src.api.inference_api:app --reload
Open Swagger UI:
http://127.0.0.1:8000/docs
 
📈 MLflow
Start MLflow:
mlflow ui
Open:
http://127.0.0.1:5000
Track:
•	AUC
•	Precision
•	Recall
•	F1
•	Threshold optimization
•	Experiment history
 
🐳 Docker
Build image:
docker build -t fraud-fastapi .
Run container:
docker run -p 8000:8000 fraud-fastapi
 
☁️ AWS Deployment
Deployment workflow:
FastAPI
   ↓
Docker
   ↓
Amazon ECR
   ↓
Amazon ECS Fargate
 
📊 Example Metrics
XGBoost Baseline
•	AUC: 0.9375
TabTransformer
•	AUC: 0.9784
Feature Store
•	Customer history: 50 transactions
•	Sequence length: 20 transactions
Platform Throughput
•	100 Transactions/sec
•	100 customers (development environment)
 
💼 Business Impact
•	Real-time detection of fraudulent behavior patterns
•	Reduced fraud investigation workload
•	Lower false positive rates
•	Improved customer experience
•	Scalable event-driven architecture
 
📌 Future Enhancements
•	Streamlit monitoring dashboard
•	Feature drift monitoring
•	Prometheus + Grafana observability
•	CI/CD pipelines using GitHub Actions
 
👨‍💻 Author
Digvijoy Nath
Engineering Manager | Machine Learning
•	IIT Madras | NIT Durgapur
•	Specialization: Forecasting, Search Ranking, Fraud detection and Real-Time ML Systems
