FROM python:3.9-alpine

ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE=todo_project.settings

WORKDIR /app

COPY . /app

RUN apk add --no-cache sqlite

RUN pip install --no-cache-dir -r requirements.txt

RUN python manage.py makemigrations

RUN python manage.py makemigrations todo_app

RUN python manage.py makemigrations todo_auth

RUN python manage.py migrate

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
