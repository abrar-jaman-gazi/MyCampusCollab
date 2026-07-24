#!/usr/bin/env bash
set -e
[ -d venv ] || python3 -m venv venv
source venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
[ -f .env ] || cp .env.example .env
printf '
Edit .env with your MySQL password and create the database first:
  mysql -u root -p < database_setup.sql

'
python manage.py makemigrations accounts marketplace collaboration communication engagement
python manage.py migrate
python manage.py seed_demo_data
python manage.py runserver
