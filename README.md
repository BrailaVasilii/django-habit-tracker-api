# Django Habit Tracker API

A Django REST Framework API for tracking personal habits with Telegram bot integration, built using Test-Driven Development (TDD) approach.

## Project Information

- **Author**: Vasili Braila
- **Email**: vbraila@gmail.com
- **GitHub**: BrailaVasilii/django-habit-tracker-api
- **Python**: 3.12
- **Development Approach**: Test-Driven Development (TDD)

## Features

- 🔐 JWT Authentication with custom User model
- 📱 Telegram bot integration
- 📊 Habit tracking and analytics
- 🔄 Celery task queue with Redis
- 🗄️ PostgreSQL database
- 🧪 Comprehensive test coverage
- 📚 API documentation with Swagger/OpenAPI

## Technology Stack

- **Backend**: Django 5.2.7, Django REST Framework 3.16.1
- **Authentication**: JWT (djangorestframework-simplejwt)
- **Database**: PostgreSQL
- **Task Queue**: Celery with Redis
- **Testing**: pytest, pytest-django, pytest-cov
- **Documentation**: drf-yasg (Swagger/OpenAPI)
- **Code Quality**: flake8
- **Dependency Management**: Poetry

## Prerequisites

- Python 3.12+
- PostgreSQL (running in Docker container `postgres-drf`)
- Redis (for Celery tasks)
- Poetry (for dependency management)

## Database Setup

The project uses a PostgreSQL database with the following configuration:
- **Database**: `habit_tracker_db`
- **User**: `habit_admin`
- **Container**: `postgres-drf`

## Installation

1. **Clone the repository**:
```bash
git clone https://github.com/BrailaVasilii/django-habit-tracker-api.git
cd django-habit-tracker-api
```

2. **Install dependencies with Poetry**:
```bash
poetry install
```

3. **Activate virtual environment**:
```bash
poetry shell
```

4. **Configure environment variables**:
Create a `.env` file based on `.env.example`:
```bash
cp .env.example .env
```

Edit `.env` with your configuration:
```env
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

DB_ENGINE=django.db.backends.postgresql
DB_NAME=habit_tracker_db
DB_USER=habit_admin
DB_PASSWORD=your-password
DB_HOST=localhost
DB_PORT=5432

CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0

TELEGRAM_BOT_TOKEN=your-telegram-bot-token
```

## Development Stages

The project is developed in phases using TDD methodology:

### ✅ Stage 0: Development Environment Setup
- Poetry dependency management
- Django project structure
- PostgreSQL integration
- Testing framework setup
- Environment configuration

### 🔄 Stage 1: User Model + Authentication (TDD)
- Custom User model with Telegram integration
- JWT authentication endpoints
- User registration and login
- Comprehensive test coverage

### 📋 Future Stages
- Habit models and CRUD operations
- Habit tracking and analytics
- Telegram bot integration
- Advanced features and optimizations

## Project Structure

```
django-habit-tracker-api/
├── config/                 # Django project settings
│   ├── settings.py
│   ├── urls.py
│   └── ...
├── users/                  # User management app
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   └── tests/
├── habits/                 # Habit tracking app
│   ├── models.py
│   ├── views.py
│   └── tests/
├── .env                    # Environment variables (not in git)
├── .env.example           # Environment template
├── pytest.ini            # Pytest configuration
├── .coveragerc           # Coverage configuration
└── manage.py
```

## Running Tests

```bash
# Run all tests with coverage
pytest

# Run specific app tests
pytest users/tests/
pytest habits/tests/

# Generate coverage report
pytest --cov=. --cov-report=html
```

## Code Quality

```bash
# Run linting
flake8

# Check Django configuration
python manage.py check
```

## Database Operations

```bash
# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Access database shell
python manage.py dbshell
```

## Development Server

```bash
# Run development server
python manage.py runserver
```

## API Documentation

Once the server is running, access the API documentation at:
- Swagger UI: `http://localhost:8000/swagger/`
- ReDoc: `http://localhost:8000/redoc/`

## Testing Database Connection

```bash
# Test PostgreSQL connection
python -c "
import psycopg2
try:
    conn = psycopg2.connect(
        host='localhost',
        port='5432',
        database='habit_tracker_db',
        user='habit_admin',
        password='your-password'
    )
    print('✅ Database connection successful!')
    conn.close()
except Exception as e:
    print(f'❌ Connection error: {e}')
"
```

## Contributing

This project follows Test-Driven Development (TDD):

1. Write failing tests (RED phase)
2. Write minimal code to pass tests (GREEN phase)
3. Refactor and optimize (REFACTOR phase)

## License

This project is developed for educational and personal use.

## Current Status

**Stage 0 Complete** ✅
- All dependencies installed
- Django project configured
- Database connection established
- Testing framework ready
- Ready for Stage 1: User Model + Authentication