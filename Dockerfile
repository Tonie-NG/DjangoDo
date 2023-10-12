FROM python:3.9


ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE=todo_project.settings

WORKDIR /app

COPY . /app

VOLUME [ "/app/db" ]

RUN python -m venv venv

RUN /app/venv/bin/activate

RUN pip install --no-cache-dir -r requirements.txt

RUN python manage.py makemigrations

RUN python manage.py migrate

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "8000"]
