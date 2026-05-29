# HabitFlow 🔥

**Build habits that actually stick.**

HabitFlow is a full-stack habit tracking web application built with Django. It features a clean, modern dark-themed UI with simple daily tracking — mark complete or skip, watch your streaks grow. No clutter, no confusion — just progress.

---

## ✨ Features

### 🌐 Landing Page
- Modern, responsive landing page introducing HabitFlow
- Clear call-to-action buttons (Start Free / Sign In)
- Feature highlights: One-Tap Tracking, Streaks, and Daily Progress

### 🔐 Authentication
- User Registration
- Secure Login / Sign In
- Sign Out functionality
- Role-based access (User / Admin)

### 👤 User Side
- **Personalized Dashboard** with welcome message and current date
- **Create New Habits** with categories (e.g., Health & Fitness)
- **Monitor Habits** with daily tracking
- **One-Tap Tracking** — Mark habits as Complete or Skip
- **Streak Counter** — Visual streak tracking with day-by-day progress
- **Stats Overview**:
  - Total Habits
  - Completed Today
  - Daily Progress (%)
  - Best Streak
- Weekly habit view (Wed–Tue)

### 🛡️ Admin Side
- **Admin Panel** with system-wide overview
- **Platform Statistics**:
  - Total Users
  - Active Today
  - Total Habits
  - Logs This Week
- **User Management**:
  - Search users by name, username, or email
  - Filter users (All Users / Active / Inactive)
  - View each user's habits and activity stats
  - **Deactivate** user accounts
  - **Delete** user accounts
- Quick switch between Admin Dashboard and personal Dashboard

---

## 🛠️ Tech Stack

- **Backend:** Django (Python)
- **Frontend:** HTML, CSS, JavaScript (Dark themed UI)
- **Database:** SQLite (development) / PostgreSQL (production)
- **Deployment:** Railway (Procfile + runtime.txt configured)

---

## 📁 Project Structure

```
habitflow/
│
├── habits/                        # Main habits app
│   ├── __pycache__/
│   ├── migrations/                # Database migrations
│   ├── static/                    # App-specific static files (CSS, JS, images)
│   ├── templates/                 # App-specific HTML templates
│   ├── templatetags/              # Custom template tags & filters
│   ├── __init__.py
│   ├── admin.py                   # Django admin registration
│   ├── apps.py                    # App configuration
│   ├── context_processors.py     # Custom context processors
│   ├── forms.py                   # Habit & user forms
│   ├── middleware.py              # Custom middleware (e.g., activity tracking)
│   ├── models.py                  # Habit, User, Logs models
│   ├── tests.py                   # Unit tests
│   ├── urls.py                    # App URL routes
│   └── views.py                   # User & admin views (dashboard, tracking, admin panel)
│
├── habittracker/                  # Project configuration
│   ├── __pycache__/
│   ├── __init__.py
│   ├── asgi.py                    # ASGI entry point
│   ├── settings.py                # Project settings
│   ├── urls.py                    # Root URL configuration
│   └── wsgi.py                    # WSGI entry point
│
├── staticfiles/                   # Collected static files (production)
├── venv/                          # Virtual environment (not committed)
│
├── .env                           # Environment variables (SECRET_KEY, DB, etc.)
├── .gitignore                     # Git ignore rules
├── apt.txt                        # System-level dependencies (Railway)
├── db.sqlite3                     # SQLite database (development)
├── manage.py                      # Django management script
├── Procfile                       # Railway/Heroku process file
├── requirements.txt               # Python dependencies
└── runtime.txt                    # Python runtime version
```

---

## 📦 Installation

### Prerequisites
- Python 3.9+
- pip
- virtualenv (recommended)

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/habitflow.git
   cd habitflow
   ```

2. **Create and activate a virtual environment**
   ```bash
   python -m venv venv
   # On Windows
   venv\Scripts\activate
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   Create a `.env` file in the root directory:
   ```env
   SECRET_KEY=your-secret-key
   DEBUG=True
   DATABASE_URL=your-database-url
   ALLOWED_HOSTS=localhost,127.0.0.1
   ```

5. **Run database migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create a superuser (Admin)**
   ```bash
   python manage.py createsuperuser
   ```

7. **Collect static files**
   ```bash
   python manage.py collectstatic
   ```

8. **Run the development server**
   ```bash
   python manage.py runserver
   ```

9. **Visit the app**
   Open your browser at `http://127.0.0.1:8000/`

---

## 🚀 Deployment (Railway)

This project is pre-configured for Railway deployment:

- **`Procfile`** — defines the web process (`gunicorn habittracker.wsgi`)
- **`runtime.txt`** — specifies the Python version
- **`apt.txt`** — defines any system-level packages
- **`requirements.txt`** — Python dependencies

### Deploy Steps
1. Push your code to GitHub
2. Connect your repo to [Railway](https://railway.app/)
3. Add environment variables in Railway dashboard
4. Railway will automatically build and deploy your app

---

## 🧭 Usage

### As a User
1. Visit the landing page and click **Get Started** or **Start Free**
2. Register a new account
3. Log in to your dashboard
4. Click **+ New Habit** to create a habit
5. Track your progress daily by clicking **Complete** or **Skip**
6. Watch your streaks grow! 🔥

### As an Admin
1. Log in with admin credentials
2. Access the **Admin Panel** from your dashboard
3. View system-wide stats and user activity
4. Search and filter users
5. Deactivate or delete user accounts as needed

---

## 🔮 Future Improvements

- Email notifications and reminders
- Habit categories customization
- Export progress data (CSV/PDF)
- Mobile app version
- Social sharing & friend challenges
- Dark/Light mode toggle

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to fork the repo and submit a pull request.

---

## 📄 License

This project is licensed under the MIT License.

---

## 👨‍💻 Author

**Herbert Adogo**
- 📧 herbsattwo@gmail.com

---

⭐ If you like this project, give it a star on GitHub!