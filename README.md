# CampusCollab

CampusCollab is a modern student freelancing and project collaboration platform built with **HTML, CSS, vanilla JavaScript, Python/Django and MySQL**. Students can present their skills, publish gigs, submit proposals, create collaboration projects, form teams, message one another and build a reviewed portfolio. Administrators receive a separate moderation and analytics workspace.

## Included functionality

- Email-based student registration, login, logout and password reset
- Custom Django user model with student/admin roles and suspension controls
- Student onboarding, profile editing, skill tags and searchable directory
- Portfolio project management with images, GitHub and live-demo links
- Gig creation, editing, filtering, saving and owner management
- Proposal submission, duplicate prevention, shortlisting, acceptance and rejection
- Collaboration project creation, filtering, join requests and team management
- Project updates, team capacity controls and progress display
- Direct messaging with AJAX sending, attachments, read state and access checks
- Notifications for proposals, teams, messages, reviews and admin actions
- Four-dimension reviews and community reports
- Student dashboard with real database statistics and recommendations
- Custom admin dashboard for users, content and moderation reports
- Responsive desktop, tablet and mobile layouts, including mobile bottom navigation
- Demo-data management command and focused Django tests

## Project structure

```text
CampusCollab/
├── campuscollab/              # Django configuration
├── apps/
│   ├── accounts/              # Users, profiles, skills, portfolios
│   ├── marketplace/           # Gigs, proposals, saved gigs
│   ├── collaboration/         # Projects, teams, join requests, updates
│   ├── communication/         # Conversations, messages, notifications
│   ├── engagement/            # Reviews, reports, admin actions
│   └── dashboard/             # Landing, student dashboard, custom admin
├── templates/                 # Page and reusable component templates
├── static/css/app.css         # Complete responsive design system
├── static/js/app.js           # Navigation, tabs, toasts and AJAX messaging
├── media/                     # User-uploaded files (created locally)
├── database_setup.sql
├── requirements.txt
└── manage.py
```

## Requirements

- Python 3.12 or newer
- MySQL 8.x or compatible MySQL server
- VS Code or another IDE
- Git is optional

## 1. Open in VS Code

Extract the ZIP, open the `CampusCollab` folder in VS Code, then open the integrated terminal.

## 2. Create and activate a virtual environment

### Windows PowerShell

```powershell
py -m venv venv
venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, run once:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

### Windows Command Prompt

```bat
py -m venv venv
venv\Scriptsctivate
```

### macOS/Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

## 3. Install packages

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## 4. Create the MySQL database

Run `database_setup.sql` in MySQL Workbench, or use:

```bash
mysql -u root -p < database_setup.sql
```

The database is created as `campuscollab` with `utf8mb4` support.

## 5. Configure environment variables

Copy the example file:

### Windows

```bat
copy .env.example .env
```

### macOS/Linux

```bash
cp .env.example .env
```

Edit `.env`:

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

For a quick interface preview without MySQL, temporarily set `DB_ENGINE=sqlite`. MySQL remains the default and intended database.

## 6. Generate migrations and database tables

```bash
python manage.py makemigrations accounts marketplace collaboration communication engagement
python manage.py migrate
```

## 7. Add realistic demo data

```bash
python manage.py seed_demo_data
```

Demo accounts:

| Role | Email | Password |
|---|---|---|
| Admin | `admin@campuscollab.local` | `Admin123!` |
| Student | `samira@campuscollab.local` | `Student123!` |
| Student | `arif@campuscollab.local` | `Student123!` |

Change these passwords before any public deployment.

## 8. Run the development server

```bash
python manage.py runserver
```

Open:

- Main application: `http://127.0.0.1:8000/`
- Student dashboard: `http://127.0.0.1:8000/dashboard/`
- Custom admin panel: `http://127.0.0.1:8000/dashboard/admin/`
- Django maintenance admin: `http://127.0.0.1:8000/django-admin/`

## Automated setup scripts

After installing MySQL and editing `.env`, you may run:

- Windows: `SETUP_WINDOWS.bat`
- macOS/Linux: `chmod +x SETUP_MAC_LINUX.sh && ./SETUP_MAC_LINUX.sh`

The scripts install dependencies, generate migrations, migrate, seed data and start the server.

## Run tests

```bash
python manage.py test
```

## Design customization

See `DESIGN_HANDOFF.md`. Exact visual values are centralized at the top of `static/css/app.css`; this makes it possible to apply Figma Dev Mode values without rewriting templates or backend code.

## Common MySQL problems

### `Access denied for user 'root'@'localhost'`

Confirm that `DB_PASSWORD` in `.env` matches the password used by:

```bash
mysql -u root -p
```

Also confirm MySQL is running.

### `Unknown database 'campuscollab'`

Run:

```bash
mysql -u root -p < database_setup.sql
```

### `No module named django`

Activate the virtual environment and install dependencies:

```bash
pip install -r requirements.txt
```

### Static images do not appear

Keep `DEBUG=True` during local development. Uploaded media files are served from `/media/` by the development URL configuration.

## Production notes

Before deployment, set `DEBUG=False`, use a strong secret key, configure production `ALLOWED_HOSTS`, serve static/media files through a web server or object storage, enable HTTPS/security cookie settings, and use a real email backend.
