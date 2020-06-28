from django.db import models

# Create your models here.

class AddToken(models.Model):
    token = models.CharField(max_length=20)
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.token
    