# Django To-Do List Application (Orbit)

A web-based task management application built with Django that allows users to create, manage, and track their tasks.

## Features

- User authentication (custom user model)
- Multiple projects per user
- Tasks scoped to a project (create, edit, delete, toggle done, search)
- Priority levels and optional due dates
- Responsive sidebar workspace UI

## Local setup

```bash
python -m venv venv
# Windows: venv\Scripts\activate
# macOS/Linux: source venv/bin/activate
pip install -r requirements.txt
mkdir data
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

Open http://127.0.0.1:8000

## Docker

```bash
docker compose up --build
```

App runs at http://localhost:8000

SQLite data is stored in the `sqlite_data` volume.

## Usage

1. Sign up / log in
2. Create a project
3. Open the project and add tasks
4. Toggle tasks done, edit, delete, or search within a project
