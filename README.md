# Djangodo

This is a simple to-do API built using the Django Rest Framework

## Features

- **Task Management**: Create, read, update, and delete tasks effortlessly through API endpoints.
- **User Authentication**: Secure your tasks by associating them with specific user accounts.

## Prerequisites

The easiest way to get this application up and running on your local machine is using docker. For that you'll need:

- Docker
- Git

## Setup

**Clone the Repository**

```
git clone https://github.com/Tonie-NG/DjangoDo.git
cd DjangoDo
```

**Build the image using Docker**

```
docker build -t djando-do .
```

**Run the contaienr from the image**

```
docker run -p 8000:8000 --name todo my-django-app
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
  - `http://127.0.0.1:8000/tasks/login` - POST - Login using you email, username and password.
