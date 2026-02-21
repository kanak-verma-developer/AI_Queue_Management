# AI Smart Queue Management System

This project is a real-time AI-based queue management system.
It detects people from image or camera, assigns tokens,
manages priority queue and shows analytics.

Features List
- People detection from image
- Live camera detection
- Priority based token system
- Manual add person
- Now serving display
- Analytics dashboard
- Export CSV and PDF
- Login and logout option

Installation Step
pip install -r requirements.txt

Run Command
streamlit run dashboard/app.py

Admin panel login
Username- admin
Password- 1234

Folder Structure
AI_QUEUE_MANAGEMENT
│
├── backend/               # Core Logic Files
│   ├── __init__.py
│   ├── database.py        # Database handling
│   ├── detection.py       # YOLO detection logic (Current file)
│   └── queue_logic.py     # Queue management calculations
│
├── dashboard/             # UI / Presentation Layer
│   ├── __init__.py
│   └── app.py             # Main application (Streamlit ya Flask)
│
├── image/                 # Input images for testing
│   └── image3.jpg
│
├── models/                # AI Model weights
│   └── yolov8n.pt
│
├── output/                # Generated reports and data
│   ├── queue_data.csv
│   ├── queue_data.pdf
│   └── queue_report.pdf
│
├── requirements.txt       # Dependencies (torch, ultralytics, etc.)
├── README.md              # Project documentation
└── .vscode/               # Editor settings

Project Technology Stack
1. Programming & Environment
Python 3.12: Core language for system logic and development.

VS Code: Primary IDE for coding and debugging.

OS & Sys: Modules for robust file path and system management.

2. AI & Computer Vision
YOLOv8 (Ultralytics): Real-time model for accurate human detection.

PyTorch: Backend framework for executing AI models on CPU/GPU.

OpenCV: Library for image processing and live video overlays.

3. Frontend & UI
Streamlit: Framework used to build the interactive Web Dashboard.

NumPy: Used for high-performance image data processing.

4. Data & Analytics
SQLite3: Database for persistent storage of queue records.

Pandas: Used for data tables, metrics, and analytics.

5. Export & Reporting
FPDF: Library used to generate automated PDF reports.

CSV: Format used for data export and Excel compatibility.

Developer Info 
Developed by: Kanak Verma
Internship Project 2026