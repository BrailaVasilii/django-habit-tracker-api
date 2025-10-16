# 🎯 Habit Tracker API

Django REST Framework API for tracking habits with automated Telegram reminders.

## 📋 Project Overview

**Course Project**: Django REST Framework Development  
**Author**: Vasili Braila  
**Email**: vbraila@gmail.com  
**Python**: 3.12  
**Approach**: TDD (Test-Driven Development)

This is a comprehensive habit tracking system that helps users build and maintain healthy habits through:
- 🔐 JWT Authentication
- 📊 Habit management (CRUD operations)
- 📱 Telegram bot notifications
- ⏰ Scheduled reminders via Celery
- 📈 Public habit sharing

---

## 🚀 Features

### ✅ Implemented
- [x] User authentication with JWT tokens
- [x] PostgreSQL database integration
- [x] REST API with Django REST Framework
- [x] CORS configuration for frontend
- [x] Test coverage > 80%
- [x] Code quality: Flake8 compliant

### 🔄 In Progress
- [ ] Custom User model with Telegram integration
- [ ] Habit model with validators
- [ ] Celery tasks for reminders
- [ ] Telegram bot integration

### 📅 Planned
- [ ] Advanced analytics
- [ ] Social features
- [ ] Mobile app support

---

## 🛠️ Tech Stack

**Backend:**
- Django 5.x
- Django REST Framework
- PostgreSQL 15
- Redis 7
- Celery

**Authentication:**
- JWT (djangorestframework-simplejwt)
- CORS headers

**Testing:**
- pytest
- pytest-django
- pytest-cov (80%+ coverage)

**Code Quality:**
- Flake8
- Poetry (dependency management)

**Integrations:**
- Telegram Bot API
- Docker (PostgreSQL, Redis)

---

## 📦 Installation

### Prerequisites
- Python 3.12+
- Poetry
- Docker (for PostgreSQL and Redis)

### Setup Steps

1. **Clone repository:**
```bash
git clone https://github.com/BrailaVasilii/django-habit-tracker-api.git
cd django-habit-tracker-api
```

2. **Install dependencies:**
```bash
poetry install
poetry shell
```

3. **Setup PostgreSQL (Docker):**
```bash
docker run --name habit-tracker-postgres \
  -e POSTGRES_DB=habit_tracker_db \
  -e POSTGRES_USER=habit_admin \
  -e POSTGRES_PASSWORD=SecureHabit2025! \
  -p 5432:5432 -d postgres:15
```

4. **Setup Redis (Docker):**
```bash
docker run --name habit-tracker-redis \
  -p 6379:6379 -d redis:7
```

5. **Environment configuration:**
```bash
cp .env.example .env
# Edit .env with your credentials
```

6. **Run migrations:**
```bash
python manage.py migrate
```

7. **Create superuser:**
```bash
python manage.py createsuperuser
```

8. **Run development server:**
```bash
python manage.py runserver
```

Access API: `http://127.0.0.1:8000/`  
Access Admin: `http://127.0.0.1:8000/admin/`  
API Docs: `http://127.0.0.1:8000/swagger/`

---

## 🧪 Testing
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=. --cov-report=html

# Run specific app tests
pytest users/tests/ -v
pytest habits/tests/ -v

# Check code quality
flake8 . --exclude=migrations
```

---

## 📚 API Documentation

### Authentication Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/users/register/` | Register new user |
| POST | `/api/users/token/` | Obtain JWT token |
| POST | `/api/users/token/refresh/` | Refresh JWT token |

### Habit Endpoints (Coming Soon)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/habits/` | List user habits |
| POST | `/api/habits/` | Create habit |
| GET | `/api/habits/{id}/` | Get habit details |
| PATCH | `/api/habits/{id}/` | Update habit |
| DELETE | `/api/habits/{id}/` | Delete habit |
| GET | `/api/habits/public/` | List public habits |

Full API documentation available at `/swagger/` and `/redoc/`

---

## 📁 Project Structure
```
django-habit-tracker-api/
├── config/              # Django settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── users/               # User authentication
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   └── tests/
├── habits/              # Habit management
│   ├── models.py
│   ├── validators.py
│   ├── serializers.py
│   ├── views.py
│   ├── tasks.py        # Celery tasks
│   └── tests/
├── manage.py
├── pyproject.toml       # Poetry dependencies
└── .env.example         # Environment template
```

---

## 🔐 Environment Variables

Create `.env` file with:
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

TELEGRAM_BOT_TOKEN=your-bot-token
```

---

## 🤝 Contributing

This is a course project. Contributions are welcome for educational purposes.

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'feat: add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

---

## 📝 Development Workflow

This project follows **GitFlow** methodology:

- `main` - Production-ready code
- `develop` - Integration branch for features
- `feature/*` - Individual features/stages

### Git Commit Convention
```
feat: new feature
fix: bug fix
docs: documentation
test: testing
refactor: code refactoring
chore: maintenance
```

---

## 📖 Course Requirements

### ✅ Acceptance Criteria

- [x] CORS configured
- [ ] Telegram integration
- [x] Pagination (5 items per page)
- [x] Environment variables
- [ ] All models implemented
- [ ] All endpoints implemented
- [ ] 5 validators configured
- [ ] Permissions configured
- [ ] Celery tasks for reminders
- [ ] Test coverage ≥ 80%
- [x] Best practices followed
- [x] Dependencies list (Poetry)
- [ ] Flake8 = 100% (excluding migrations)
- [x] GitHub repository

---

## 📧 Contact

**Vasili Braila**  
Email: vbraila@gmail.com  
GitHub: [@BrailaVasilii](https://github.com/BrailaVasilii)

---

## 📄 License

This project is created for educational purposes as part of a Django REST Framework course.

---

## 🙏 Acknowledgments

- Django REST Framework documentation
- Telegram Bot API
- Course instructors and mentors

---

**⭐ If you find this project useful, please consider giving it a star!**