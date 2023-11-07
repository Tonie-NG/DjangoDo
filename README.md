# Djangodo

This is a simple to-do API built using the Django Rest Framework

## Features

- **Task Management**: Create, read, update, and delete tasks effortlessly through API endpoints.
- **User Authentication**: Secure your tasks by associating them with specific user accounts.

## Prerequisites

The easiest way to get this application up and running on your local machine is using docker. For that you'll need:

- Docker
- Docker Compose
- Git

## Setup

**Clone the Repository**

```
git clone https://github.com/Tonie-NG/DjangoDo.git djangodo
cd djangodo
```

**Create a `.env` file in treh root directory and provide the following variables**

```
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'youremailaddress'
EMAIL_HOST_PASSWORD = 'your email app-password'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'


CELERY_BROKER_URL = "redis://redis:6379/0" // or a url to your own redis instance

```

**Build the and run the application using docker compose**

```
docker compose up
```

This command will build the Docker image and start the container. The application will be accessible at http://127.0.0.1:8000/

_Note that the names `django-do` and `todo` are optional and you can replace it if you wish_

## API Endpoints

- Tasks

  - `http://127.0.0.1:8000/tasks` - GET - Retrieve all tasks.
  - `http://127.0.0.1:8000/tasks` - POST - Create a new task.

- Task

  - `http://127.0.0.1:8000/tasks/<id>` - GET - Retrieve a task using its id.
  - `http://127.0.0.1:8000/tasks/<id>` - PUT- Update a task using its id.
  - `http://127.0.0.1:8000/tasks/<id>` - PATCH- Update a task using its id.
  - `http://127.0.0.1:8000/tasks/<id>` - PUT- Delete a task using its id.

- User
  - `http://127.0.0.1:8000/tasks/signup` - POST - Register a new user.
  - `http://127.0.0.1:8000/tasks/login` - POST - Login using your email, username and password.
