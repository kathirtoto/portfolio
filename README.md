# Kathiresan K - Full-Stack Personal Portfolio Website

A modern, responsive, full-stack personal portfolio website designed for **Kathiresan K**, a Computer Science and Engineering student at **Rajalakshmi Engineering College**.

Built with a **React + Vite** frontend, a **Python Flask** REST API backend, **MySQL** database persistence, and verified **SMTP email notifications**.

---

## 👨‍💻 Profile Summary

- **Name:** Kathiresan K
- **Institution:** Rajalakshmi Engineering College
- **Degree:** B.E. Computer Science and Engineering
- **Current Status:** Computer Science Engineering Student
- **Phone:** [+91 9566741512](tel:9566741512)
- **Email:** [kathiresantoto@gmail.com](mailto:kathiresantoto@gmail.com)
- **LinkedIn:** [linkedin.com/in/kathiresan-toto-327564364/](https://www.linkedin.com/in/kathiresan-toto-327564364/)
- **Programming Languages:** C, C++, Java, Python (Foundational & Core Basics)
- **Frontend Technologies:** HTML, CSS, JavaScript, React.js (Actively Learning & Practicing)

---

## 📂 Project Architecture

```
personal-portfolio/
├── frontend/                     # React.js + Vite Application
│   ├── public/
│   │   └── assets/
│   │       └── profile.jpg       # Profile photo
│   ├── src/
│   │   ├── components/
│   │   │   ├── Navbar.jsx        # Navigation with active link highlighting & mobile menu
│   │   │   ├── Hero.jsx          # Hero section with clean circular photo & LinkedIn link
│   │   │   ├── About.jsx         # Authentic student developer biography
│   │   │   ├── Education.jsx     # Rajalakshmi Engineering College academic details
│   │   │   ├── Skills.jsx        # Honest skill cards grouped by domain (no fake percentages)
│   │   │   ├── Achievements.jsx  # Prepared section for hackathons, workshops & certs
│   │   │   ├── Contact.jsx       # Contact form with strict error handling & LinkedIn card
│   │   │   └── Footer.jsx        # Footer with back-to-top navigation & LinkedIn link
│   │   ├── App.jsx               # Main React application shell
│   │   ├── App.css               # Modern dark-themed CSS design system
│   │   └── main.jsx              # Vite entry point
│   ├── index.html                # Custom SEO title and metadata
│   ├── package.json              # Frontend dependencies and build scripts
│   └── vite.config.js            # Vite configuration with backend API proxy
│
├── backend/                      # Python Flask REST API
│   ├── app.py                    # Flask application factory and route registration
│   ├── config.py                 # Configuration loader (MySQL, SQLite, SMTP settings)
│   ├── database.py               # SQLAlchemy database initialiser
│   ├── models/
│   │   └── message.py            # Message database model
│   ├── routes/
│   │   └── contact.py            # POST /api/contact with DB save & strict SMTP dispatch
│   ├── requirements.txt          # Python dependencies
│   ├── .env.example              # Template for environment variables
│   └── .env                      # Local environment configuration
│
├── database/
│   └── portfolio.sql             # Production MySQL schema for messages table
│
├── README.md                     # Comprehensive documentation and deployment guide
└── .gitignore                    # Git ignore file for node_modules, .env, DBs, and caches
```

---

## 🚀 Quick Start & Local Development

### 1. Prerequisites
- **Node.js** (v18 or higher) & `npm`
- **Python** (v3.10 or higher) & `pip`
- **MySQL Server** (Optional for local testing — SQLite fallback is enabled automatically)

---

### 2. Backend Setup (Flask API)

1. Open a terminal in the project root:
   ```bash
   cd backend
   ```

2. Create and activate a Python virtual environment:
   ```bash
   # On Windows:
   python -m venv venv
   venv\Scripts\activate

   # On macOS/Linux:
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure your `.env` file:
   ```bash
   # Copy the example configuration
   cp .env.example .env
   ```
   Edit `.env` with your Gmail App Password to receive real emails.

5. Start the Flask backend server:
   ```bash
   python app.py
   ```
   The backend API will run on `http://localhost:5000`.

---

### 3. Frontend Setup (React + Vite)

1. Open a new terminal and navigate to the `frontend` folder:
   ```bash
   cd frontend
   ```

2. Install frontend dependencies:
   ```bash
   npm install
   ```

3. Start the Vite development server:
   ```bash
   npm run dev
   ```
   Open your browser and navigate to `http://localhost:5173`.

---

## 📧 Real Email Notification Setup (Gmail SMTP)

When a visitor submits the contact form:
1. React sends form data to `POST /api/contact`.
2. Flask validates the input and persists the submission into the `messages` table.
3. Flask sends an email notification directly to **`kathiresantoto@gmail.com`**.
4. If email delivery fails, the backend truthfully returns `500` error:
   ```json
   { "success": false, "message": "Message could not be sent. Please try again later." }
   ```
5. Only upon successful SMTP delivery does the backend return:
   ```json
   { "success": true, "message": "Your message has been sent successfully." }
   ```

### Enabling Real Email Delivery (Takes 30 seconds):
1. Go to your **Google Account** > **Security** > **2-Step Verification** > **App Passwords** ([https://myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords)).
2. Type **"Portfolio"** and click **Create**.
3. Copy the **16-letter App Password**.
4. Add it to `backend/.env`:
   ```env
   EMAIL_HOST=smtp.gmail.com
   EMAIL_PORT=587
   EMAIL_USE_TLS=True
   EMAIL_USERNAME=kathiresantoto@gmail.com
   EMAIL_PASSWORD=your_16_letter_app_password
   EMAIL_FROM="Kathiresan K Portfolio <kathiresantoto@gmail.com>"
   EMAIL_TO=kathiresantoto@gmail.com
   ```

---

## 🗄️ Database Setup (MySQL)

### Importing the Schema into MySQL
1. Run the SQL script located in `database/portfolio.sql`:
   ```sql
   source database/portfolio.sql;
   ```
2. In your `backend/.env` file, set your `DATABASE_URL`:
   ```env
   DATABASE_URL=mysql+pymysql://<username>:<password>@localhost:3306/portfolio_db
   ```
3. If `DATABASE_URL` is omitted, the Flask backend will automatically use SQLite (`portfolio.db`).

---

## 🌐 Deployment Instructions

### 1. Frontend (Vercel / Netlify)
- **Vercel:** Import your GitHub repository, select `frontend` directory, preset **Vite**, and deploy.

### 2. Backend (Render / Railway / PythonAnywhere)
- **Render:** Connect repository, select `backend` directory, start command `python app.py` or `gunicorn app:app`, and set environment variables.

---

## 📄 License
This project is open-source and available under the [MIT License](LICENSE).
