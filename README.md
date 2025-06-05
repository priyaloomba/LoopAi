LoopAI - Data Ingestion API
This is a FastAPI-based microservice designed for data ingestion as part of the LoopAI system.

Features
RESTful API built using FastAPI
Modular and lightweight
Ready for deployment with uvicorn
Project Structure
LoopAI/
└── 
    ├── main.py               # Entry point for the FastAPI app
    ├── requirements.txt      # Python dependencies
    └── venv/                 # Local virtual environment (not recommended for version control)
Getting Started
1. Clone the Repository
git clone <repository-url>

2. Set Up Environment
Create a virtual environment (recommended):

python3 -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
Install dependencies:

pip install -r requirements.txt
3. Run the Application
uvicorn main:app --reload
Access the API at: http://localhost:8000
