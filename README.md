# 🌿 Plant Disease Detection Web App

A full-stack AI-powered web application for detecting plant diseases from leaf images.
Built with **React**, **Flask**, and **PyTorch**.

## 🚀 Features
- **AI Diagnosis**: Upload leaf images to detect diseases with >90% accuracy.
- **Confidence Score**: Rejects non-leaf images or low-confidence predictions.
- **Secure Auth**: User registration & login (JWT).
- **History**: View past predictions.
- **Responsive UI**: Glassmorphism design suitable for mobile & desktop.

## 🛠️ Tech Stack
- **Frontend**: React (Vite), CSS3 (Glassmorphism), Lucide Icons.
- **Backend**: Flask, SQLAlchemy (SQLite/MySQL), JWT.
- **AI Model**: PyTorch (MobileNetV2), trained on PlantVillage dataset.

## 📂 Project Structure
```
plant/
├── backend/            # Flask API & DB
│   ├── app.py          # Main entry point
│   ├── models.py       # Database Schema
│   ├── ml_utils.py     # Inference Logic
│   └── uploads/        # Stored images
├── frontend/           # React App
│   ├── src/
│   │   ├── pages/      # Home, Login, History
│   │   ├── components/ # Navbar, DragDrop
│   │   └── context/    # Auth Logic
└── model/              # PyTorch Model & Class Indices
```

## ⚡ How to Run

### Prerequisite
Ensure you have Python 3.9+ and Node.js installed.

### 1. Backend Setup
```bash
# Activate Virtual Environment (if not active)
.venv\Scripts\activate

# Install Dependencies
pip install -r requirements.txt

# Run Server
cd backend
python app.py
```
*Server runs on http://localhost:5000*

### 2. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```
*Client runs on http://localhost:5173*

## 📜 API Endpoints
- `POST /api/register` - Create account
- `POST /api/login` - Get JWT Token
- `POST /api/predict` - Upload Image & Get Result
- `GET /api/history` - Get User's Past Predictions

## 🧪 Model Details
- **Architecture**: MobileNetV2
- **Input**: 160x160 RGB Images
- **Threshold**: 60% Confidence Rejection
