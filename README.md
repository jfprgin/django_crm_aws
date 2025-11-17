# Simple DJango CRUD CRUD Application

This is a simple Django CRUD (Create, Read, Update, Delete) application that demonstrates the basic functionalities of a web application using the Django framework. The application allows users to create, view, update, and delete records in a database.

## Features
- Create new records
- View a list of all records
- Update existing records
- Delete records
- Simple and user-friendly interface

## Tech Stack
- **Backend Framework**: Django (Python)
- **Database**: PostgreSQL
- **Frontend**: Bootstrap (for styling)
- **Environment Management**: Pipenv
- **Version Control**: Git/GitHub

## Setup Instructions for Local Development in PyCharm

### 1. Clone the Repository
```bash
git clone <repository_url>
cd home_budget
```

### 2. Setup Python Virtual Environment
Make sure you are in the project root directory and install `pipenv` and activate the virtual environment:

```bash
pipenv shell
```
- You will get something like `/home/<local_user>/.local/share/virtualenvs/home_budget-<random_string>/bin/activate`, save it.

### 3. Install Dependencies
```bash
pipenv install
```

### 4. Configure Python Interpreter in PyCharm
1. Go to **Settings > Python > Interpreter**.
2. Click **Add Interpreter** > **Add Local Interpreter** > **Select Existing**.
3. In  **Browse** paste the `/home/<local_user>/.local/share/virtualenvs/home_budget-<random_string>/bin/activate` and choose `python3.12`:

### 5. Configure Django Settings
1. Go to **Settings > Python > Django**
2. In **"Settings: "** find the `settings` *directory*, and select it.
3. in **"Manage script: "** find `manage.py`, and select it.

### 6. Configure Environment Variables
1. Go to **Run > Edit Configurations** (top right).
2. Under **Environment variables**, set:
   ```
   PYTHONUNBUFFERED=1;DJANGO_SETTINGS_MODULE=settings
   
   ```
3. Go to the `settings` directory, find `local_settings.py.template`, copy it and remove `.template`.

### 7. Database Setup
1. Set up the database (PostgreSQL).
2. Run migrations:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```
3. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```
   
### 8. Running the Development Server
To start the server:
```bash
python manage.py runserver
```

## Contact
If you have any questions or suggestions, feel free to reach out to:
- **Email**: jfprgin@gmail.com
