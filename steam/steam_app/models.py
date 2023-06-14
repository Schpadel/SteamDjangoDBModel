from django.db import models


# Create your models here.
class Game(models.Model):
    name = models.CharField(max_length=200)
    release_date = models.DateTimeField("date released")
