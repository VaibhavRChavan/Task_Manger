```markdown
# 🗂️ Task Manager Web Application

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-5.0-092E20?style=for-the-badge&logo=django&logoColor=white)
![MongoDB](https://img.shields.io/badge/MongoDB-4.4%2B-47A248?style=for-the-badge&logo=mongodb&logoColor=white)
![Tailwind](https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white)

A modern and user-friendly **Task Management Web Application** designed to help users efficiently create, organize, and track their tasks.  
The application follows a **clean, modular architecture** with a responsive frontend and a secure backend powered by **Django Authentication** and **MongoDB**.

---

## 📑 Table of Contents
- [📌 Overview](#-overview)
- [📸 Screenshots](#-project-screenshots)
- [🚀 Key Features](#-key-features)
- [🛠️ Technology Stack](#-technology-stack)
- [🏗️ Architecture](#-architecture-highlights)
- [💻 Installation & Setup](#-project-setup-guide)
- [👨‍💻 Author](#-author)

---

## 📌 Overview

The Task Manager application allows users to securely register, log in, and manage their personal tasks. Each user has **fully isolated task data**, ensuring privacy and data integrity.

The project is built using modern web technologies with a focus on:
- 🔐 **Security** (Authentication & Authorization)
- 📈 **Scalability** (MongoDB NoSQL Database)
- 🧩 **Maintainability** (Modular Django Apps)
- 🎨 **Usability** (Clean Tailwind UI)

---

## 📸 Project Screenshots

### 🔐 User Authentication

**Login Page**
![Login Page](images/Login.jpeg)

**Register Page**
![Register Page](images/Register.jpeg)

### 📊 Dashboard & Tasks

**Dashboard Overview**
![Dashboard](images/Dashbord.jpeg)

**Task Management**
![Task Management](images/Tasks.jpeg)

### 🗄️ Database Structure

**MongoDB Compass View**
![MongoDB Compass View](images/MongoDB.jpeg)

---

## 🚀 Key Features

### 👤 Authentication
* User Registration & Login
* Secure Session-based Authentication
* Route protection using `@login_required` decorator

### 📝 Task Management
* **CRUD Operations:** Create, Read, Update, and Delete tasks.
* **Attributes:** Title, description, priority (Low/Medium/High), and due date.
* **Status Tracking:** Mark tasks as **Completed** or **Pending**.
* **Bulk Actions:** Clear all completed tasks.

### 📊 Dashboard & Filtering
* **Real-time Statistics:** Counters for Total, Pending, and Completed tasks.
* **Smart Filtering:** Filter by All, Pending, Completed, or High Priority.

### 🔒 Security & Data Isolation
* **User Isolation:** Tasks are stored per user; users cannot access others' data.
* **Secure Queries:** MongoDB queries utilize strict user-based filtering.

### 🎨 UI & UX
* **Responsive:** Optimized for Desktop and Mobile.
* **Styling:** Modern styling with Tailwind CSS and gradient accents.
* **Feedback:** Toast notifications for success/error actions.

---

## 🛠️ Technology Stack

| Category | Technologies |
| :--- | :--- |
| **Frontend** | HTML5, Tailwind CSS, JavaScript (Vanilla) |
| **Backend** | Python, Django Framework, Django Auth |
| **Database** | MongoDB (NoSQL), PyMongo Driver |
| **Tools** | Git, VS Code, Postman |

---

## 🏗️ Architecture Highlights

* **Hybrid Setup:** Uses Django's SQL (SQLite) for User Auth/Sessions and MongoDB for Task Data.
* **No ORM for Tasks:** Direct **PyMongo** usage for high-performance NoSQL operations.
* **RESTful Approach:** Backend communicates with the frontend via standard HTTP methods.

---

## 🖥️ Project Setup Guide

Follow these steps to run the project locally.

### ✅ Prerequisites
* **Python 3.10+**
* **MongoDB Community Server** (Running locally)
* **Git**

### 📥 Step 1: Clone the Repository

```bash
git clone [https://github.com/](https://github.com/)<your-github-username>/task-manager.git
cd task-manager

```

### 🐍 Step 2: Create Virtual Environment

**Windows:**

```bash
python -m venv venv
venv\Scripts\activate

```

**macOS / Linux:**

```bash
python3 -m venv venv
source venv/bin/activate

```

### 📦 Step 3: Install Dependencies

```bash
pip install -r requirements.txt

```

### 🗄️ Step 4: Configure MongoDB

1. Start your **MongoDB Community Server**.
2. Open `config/settings.py` and ensure the database settings utilize your local instance:

```python
# config/settings.py

# MongoDB Connection
MONGODB_URI = "mongodb://localhost:27017"
MONGODB_NAME = "task_manager_db"

```

### 🧩 Step 5: Apply Migrations

*Note: This creates the SQLite tables for Django's built-in Authentication system.*

```bash
python manage.py makemigrations
python manage.py migrate

```

### 👤 Step 6: Create Superuser (Optional)

To access the Django Admin panel:

```bash
python manage.py createsuperuser

```

### ▶️ Step 7: Run the Server

```bash
python manage.py runserver

```

Open your browser and visit:

👉 **http://127.0.0.1:8000/**

---

## 🚀 Future Enhancements

* [ ] Task categories & tags
* [ ] Email verification
* [ ] Drag-and-drop task ordering
* [ ] Docker Support

---

## 👨‍💻 Author

**Vivek** *Built as a real-world Django + MongoDB full-stack project.*

```

```