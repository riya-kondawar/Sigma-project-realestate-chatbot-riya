# 🏠 Real Estate Analysis Chatbot

AI-powered real estate trend analysis with **React + Django + OpenAI**.

---

## ✨ Features

* **AI-Generated Insights** using OpenAI GPT-4o-mini
* **Excel Upload & Processing** (Pandas)
* **Automatic Locality Detection** from user query
* **Interactive Charts** (Recharts)
* **Download Filtered Data as CSV**
* **Clean, Responsive UI** with scroll-based layout
* **REST API Backend** (Django + DRF)

---

## 🛠 Tech Stack

### Frontend

* React 18
* Bootstrap 5
* Recharts
* Axios

### Backend

* Django 4.2
* Django REST Framework
* Pandas
* OpenAI API
* SQLite (Dev) / PostgreSQL (Prod)

---

## 🚀 Getting Started

### 1️⃣ Backend Setup

```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Create `.env`:

```
OPENAI_API_KEY=your-key
```

### 2️⃣ Frontend Setup

```bash
cd frontend
npm install
npm start
```

---

## 📸 Screenshots

![Dashboard](/assets/ss1.png)
![AI Summary](/assets/data.png)
![Charts & Table](/assets/charts.png)

---

## 📁 Project Structure

```
backend/
frontend/
assets/
```

---
