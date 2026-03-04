<div align="center">

# 🧠 Health AI — Neural Diagnostic Platform

<br/>

**Medical-grade, AI-powered preliminary health diagnosis.**
A full-stack SaaS platform that uses machine learning to analyze symptoms and predict possible conditions in real-time.

<br/>

![Tech Stack](https://img.shields.io/badge/Backend-Flask%20%7C%20Python-005571?style=for-the-badge&logo=flask)
![Frontend](https://img.shields.io/badge/Frontend-React%20%7C%20TypeScript-61DAFB?style=for-the-badge&logo=react)
![ML](https://img.shields.io/badge/ML-Scikit--Learn%20%7C%20SHAP-F7931E?style=for-the-badge&logo=scikit-learn)
![Database](https://img.shields.io/badge/Database-SQLite%20%7C%20SQLAlchemy-003B57?style=for-the-badge&logo=sqlite)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

<br/>

</div>

---

## ✨ Features

| Category | Feature |
|---|---|
| 🤖 **AI Engine** | Multi-class disease prediction using a trained classifier on 40+ symptoms |
| 📊 **Explainability** | SHAP-powered model explanations so users understand *why* a result was given |
| 🔐 **Secure Auth** | JWT access + refresh tokens, email OTP verification, RBAC |
| 📈 **History Dashboard** | Full diagnostic history with risk-level tracking and report visualization |
| 🎨 **Premium UI** | SaaS-grade design with Framer Motion animations, glassmorphism & Unsplash imagery |
| 🛡️ **Rate Limiting** | Per-IP request throttling with `flask-limiter` to prevent abuse |
| 📧 **Email Notifications** | OTP delivery via SMTP (Gmail) using `flask-mail` |
| 🐳 **Docker Ready** | Full `docker-compose.yml` for local and production deployment |
| 🧪 **Test Suite** | Pytest-based unit and integration tests |

---

## 🖼️ Preview

> *The platform features a dark clinical aesthetic, staggered animations, and a responsive layout across all devices.*

| **Hero Section** | **Analyze Page** | **History Dashboard** |
|:---:|:---:|:---:|
| Full-viewport parallax hero with floating AI status card | Split-screen symptom selector with category grouping | Diagnostic vault with stats bar and risk-level cards |

---

## 🏗️ Architecture

```
health_AI/
├── backend/                   # Flask REST API
│   ├── app.py                 # Application factory
│   ├── config.py              # Environment configurations
│   ├── extensions.py          # Flask extensions (db, jwt, limiter, cache, mail)
│   ├── models/                # SQLAlchemy models (User, Analysis, OTP)
│   ├── routes/
│   │   ├── auth.py            # Register, Login, OTP Verify endpoints
│   │   └── predict.py         # /analyze, /history, /analysis/<id>
│   ├── services/
│   │   ├── auth_service.py    # JWT, OTP, user management logic
│   │   └── explain_service.py # SHAP model explainability
│   ├── ml_models/
│   │   ├── model.pkl          # Trained disease classifier
│   │   └── symptom_columns.pkl
│   └── schemas/               # Marshmallow validation schemas
│
├── frontend/                  # React + TypeScript (Vite)
│   └── src/
│       ├── pages/
│       │   ├── HomePage.tsx        # Landing page with animations
│       │   ├── AnalyzePage.tsx     # Symptom selection + AI call
│       │   ├── HistoryPage.tsx     # Diagnostic dashboard
│       │   ├── ResultsPage.tsx     # Detailed results with SHAP
│       │   ├── LoginPage.tsx       # Split-screen auth
│       │   └── RegisterPage.tsx    # Split-screen registration
│       ├── components/
│       │   └── Layout.tsx          # Navbar + Footer
│       └── contexts/
│           └── AuthContext.tsx     # Global auth state
│
├── train_model.py             # Model training script
├── docker-compose.yml         # Container orchestration
├── Makefile                   # Dev shortcuts
└── setup.ps1 / setup.sh       # One-command setup scripts
```

---

## 🚀 Quick Start

### Prerequisites

- **Python** 3.10+
- **Node.js** 18+
- **Git**

---

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/health_AI.git
cd health_AI
```

---

### 2. Backend Setup

```bash
cd backend

# Create and activate virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS/Linux

# Install dependencies
pip install -r requirements.txt
```

#### Configure Environment Variables

Copy `.env.example` to `.env` and fill in the values:

```bash
cp ../.env.example backend/.env
```

```env
# Flask
SECRET_KEY=your-secret-key
FLASK_ENV=development
DEBUG=true

# JWT
JWT_SECRET_KEY=your-jwt-secret

# Database (SQLite default)
DATABASE_URL=sqlite:///medical_diagnosis.db

# Gmail SMTP (for OTP emails)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
SMTP_FROM=your-email@gmail.com
```

#### Run the Backend

```bash
flask run -h 0.0.0.0 -p 5000
```

> The API will be available at `http://localhost:5000`

---

### 3. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start the dev server
npm run dev
```

> The app will be available at `http://localhost:5173`

---

### 4. Docker (Optional)

Run the entire stack with one command:

```bash
docker-compose up --build
```

---

## 📡 API Reference

### Authentication

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/v1/auth/register` | Register a new user |
| `POST` | `/api/v1/auth/login` | Login and receive JWT tokens |
| `POST` | `/api/v1/auth/verify-2fa` | Verify OTP and complete login |

### Prediction

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| `POST` | `/api/v1/predict/analyze` | ✅ JWT | Submit symptoms, receive diagnosis |
| `GET` | `/api/v1/predict/history` | ✅ JWT | Fetch past analyses |
| `GET` | `/api/v1/predict/analysis/<id>` | ✅ JWT | Get a specific analysis by ID |

#### Example Request: `/api/v1/predict/analyze`

```json
POST /api/v1/predict/analyze
Authorization: Bearer <access_token>

{
  "symptoms": "Fever, Cough, Fatigue, Headache"
}
```

#### Example Response

```json
{
  "analysis_id": "a3b8d1b6-...",
  "prediction": "Pneumonia",
  "probability": 82.5,
  "risk": "High",
  "top_diseases": [
    { "disease": "Pneumonia", "probability": 82.5 },
    { "disease": "Bronchial Asthma", "probability": 11.2 },
    { "disease": "Tuberculosis", "probability": 6.3 }
  ],
  "matched_symptoms": ["fever", "cough", "fatigue"],
  "doctor": "Pulmonologist",
  "explanation": { ... }
}
```

---

## 🧪 Running Tests

```bash
cd backend

# Run all tests
pytest

# Run with coverage report
pytest --cov=. --cov-report=html
```

---

## 🔒 Security Design

- **JWT tokens** — Short-lived access tokens (24h) + long-lived refresh tokens (30d)
- **Email OTP** — Verification required for new account activation
- **Password Hashing** — `bcrypt`-based hashing, never stored in plain text
- **Rate Limiting** — Per-IP limits via `flask-limiter`, OPTIONS preflight excluded
- **CORS** — Restricted to known frontend origins

---

## 📦 Tech Stack

### Backend
| Library | Purpose |
|---|---|
| `Flask` | Web framework |
| `Flask-JWT-Extended` | JWT authentication |
| `Flask-SQLAlchemy` | ORM & database management |
| `Flask-Mail` | Email / OTP delivery |
| `Flask-Limiter` | API rate limiting |
| `Flask-CORS` | Cross-origin resource sharing |
| `Scikit-Learn` | ML model & predictions |
| `SHAP` | Model explainability |
| `Marshmallow` | Request/response validation |
| `Gunicorn` | Production WSGI server |

### Frontend
| Library | Purpose |
|---|---|
| `React 18` + `TypeScript` | UI framework |
| `Vite` | Build tool & dev server |
| `Material UI (MUI)` | Component library |
| `Framer Motion` | Animations & transitions |
| `React Router v6` | Client-side routing |
| `Axios` | HTTP client |

---

## 🤝 Contributing

Contributions are welcome! Please read [`CONTRIBUTING.md`](CONTRIBUTING.md) before submitting a pull request.

1. Fork the repository
2. Create your feature branch: `git checkout -b feature/amazing-feature`
3. Commit your changes: `git commit -m 'feat: add amazing feature'`
4. Push to the branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

---

## 📄 License

This project is licensed under the **MIT License** — see the [`LICENSE`](LICENSE) file for details.

---

## ⚠️ Disclaimer

> Health AI is an educational and research project. The AI-generated results are intended as **preliminary guidance only** and should **not** replace professional medical advice, diagnosis, or treatment. Always consult a qualified healthcare provider.

---

<div align="center">

Made with ❤️ for better health outcomes

</div>
