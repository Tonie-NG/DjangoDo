FROM python:3.9-alpine

ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE=todo_project.settings

WORKDIR /app

COPY . /app

RUN apk add --no-cache sqlite

RUN pip install --no-cache-dir -r requirements.txt

RUN python manage.py makemigrations

RUN python manage.py migrate

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
