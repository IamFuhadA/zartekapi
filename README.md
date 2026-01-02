# Zartak Ride Sharing API

A simple Django REST API for ride sharing.

## Setup

```bash
# Create virtual environment
python -m venv .venv
.venv\Scripts\activate  # Windows

# Install dependencies
pip install django djangorestframework

# Run migrations
python manage.py migrate

# Start server
python manage.py runserver
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/user/register/` | Register a new user |
| POST | `/api/ride/` | Create a new ride |
| GET | `/api/ride/` | List all rides |
| GET | `/api/ride/<id>` | Get ride details |

## Run Tests

```bash
python manage.py test
```
