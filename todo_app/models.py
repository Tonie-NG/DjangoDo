from django.db import models
# from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from datetime import datetime


class Todo(models.Model):
    # user = models.foreignkey(user, on_delete=models.cascade())
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    completed = models.BooleanField(default=False)
    to_be_completed = models.DateField(validators=[MinValueValidator(limit_value=datetime.now().date())])
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return self.title
# Create your models here.
