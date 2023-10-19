from django.db import models

# Create your models here.
class User(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=200, null=False, unique=True)
    email = models.CharField(max_length=200, null=False, unique=True)
    password = models.CharField(max_length=200, null=False)
    created_at = models.DateField(auto_now_add=True, null=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return self.username
