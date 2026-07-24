@echo off
setlocal
if not exist venv (
  py -m venv venv
)
call venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
if not exist .env copy .env.example .env
echo.
echo Edit .env with your MySQL password, then make sure the campuscollab database exists.
echo Run database_setup.sql in MySQL Workbench or: mysql -u root -p ^< database_setup.sql
echo.
python manage.py makemigrations accounts marketplace collaboration communication engagement
python manage.py migrate
python manage.py seed_demo_data
python manage.py runserver
endlocal
