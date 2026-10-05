# 🎓 CampusCollab

> A full-stack university collaboration marketplace where students can showcase skills, discover paid gigs, submit proposals, create projects, recruit teammates, communicate, and build a reviewed portfolio.

**Tech Stack:** Python · Django 6 · MySQL · HTML5 · CSS3 · JavaScript

🌐 **Live Demo:** http://campuscollab-five.vercel.app/

## 📌 Project Overview

CampusCollab is designed as a single platform for university students to find opportunities and collaborate with other students. It combines marketplace features, project/team management, communication, notifications, reviews, dashboards, and administration in one Django application.

## ✨ Main Features

- 🔐 Student registration, login, logout, password reset, and role-based access
- 👤 Student profiles, skills, searchable directory, and portfolios
- 💼 Gig creation, filtering, saving, and management
- 📩 Proposal submission, shortlisting, acceptance, and rejection
- 🤝 Collaboration projects, teams, join requests, and project updates
- 💬 Direct messaging with AJAX, attachments, read state, and access checks
- 🔔 Notifications for proposals, teams, messages, reviews, and admin actions
- ⭐ Four-dimension reviews and community reports
- 📊 Student dashboard with database-driven statistics
- 🛡️ Custom admin dashboard for users, content, and moderation
- 📱 Responsive desktop, tablet, and mobile interface
- 🧪 Django tests and demo-data management

## 🛠️ Main Technologies

| Technology | Purpose |
|---|---|
| Python | Backend programming |
| Django 6 | Web framework and application logic |
| MySQL 8 | Relational database |
| HTML5 | Page structure |
| CSS3 | Responsive UI and styling |
| JavaScript | Client-side interactions and AJAX |
| PyMySQL | MySQL database driver |
| Pillow | Image processing |
| python-dotenv | Environment configuration |

## 📦 Dependencies

```txt
Django==6.0.6
PyMySQL>=1.1,<2
Pillow>=11,<13
python-dotenv>=1.0,<2
```

## 🚀 Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/abrar-jaman-gazi/MyCampusCollab.git
cd MyCampusCollab
```

### 2. Create and activate a virtual environment

**macOS/Linux**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows**
```powershell
py -m venv venv
venv\\Scripts\\Activate.ps1
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configure MySQL

Create the `campuscollab` database using `database_setup.sql`, then create a `.env` file:

```env
SECRET_KEY=replace-with-a-long-random-value
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
DB_ENGINE=mysql
DB_NAME=campuscollab
DB_USER=root
DB_PASSWORD=YOUR_MYSQL_PASSWORD
DB_HOST=127.0.0.1
DB_PORT=3306
```

### 5. Run migrations

```bash
python manage.py makemigrations accounts marketplace collaboration communication engagement
python manage.py migrate
```

### 6. Optional: Load demo data

```bash
python manage.py seed_demo_data
```

### 7. Start the server

```bash
python manage.py runserver
```

Open **http://127.0.0.1:8000/**.

### 8. Run tests

```bash
python manage.py test
```

## 🔗 Relevant Links

- 🌐 **Live Demo:** http://campuscollab-five.vercel.app/
- 💻 **GitHub:** https://github.com/abrar-jaman-gazi/MyCampusCollab

## 📁 Project Structure

```text
CampusCollab/
├── campuscollab/              # Django configuration
├── apps/
│   ├── accounts/              # Users, profiles, skills, portfolios
│   ├── marketplace/           # Gigs, proposals, saved gigs
│   ├── collaboration/         # Projects, teams, join requests
│   ├── communication/         # Messages and notifications
│   ├── engagement/            # Reviews and reports
│   └── dashboard/             # Landing, student dashboard, admin
├── templates/
├── static/
├── media/
├── database_setup.sql
├── requirements.txt
└── manage.py
```

## 👨‍💻 Author

**Abrar Jaman Gazi**

Computer Science Student — United International University (UIU)
