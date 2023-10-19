from django.db import models
# from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from datetime import datetime
from todo_auth.models import User

class Todo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50)
    description = models.CharField(null=False, max_length=800)
    completed = models.BooleanField(default=False)
    to_be_completed = models.DateField(validators=[MinValueValidator(limit_value=datetime.now().date())], null=False)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return self.title
