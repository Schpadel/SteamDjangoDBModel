from django.db import models


# Create your models here.
class Game(models.Model):
    name = models.CharField(max_length=200, default="Undefined")
    genre = models.CharField(max_length=200)
    publisher = models.CharField(max_length=200, default="Undefined")
    developer = models.CharField(max_length=200, default="Undefined")
    franchise = models.CharField(max_length=200, null=True)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    size = models.DecimalField(decimal_places=2, max_digits=100)
    rating = models.SmallIntegerField()
    release_date = models.DateTimeField("date released")
    usk = models.SmallIntegerField()
    supported_platforms = models.CharField(max_length=200, default="PC")
    supported_languages = models.CharField(max_length=200, default="EN")
    description = models.CharField(max_length=20_000, null=True)

    class Meta:
        constraints = [models.CheckConstraint(name="Test Int Constraint", check=models.Q(rating__range=(0, 100)), )]


class Library(models.Model):
    timePlayed = models.DateTimeField()
    lastPlayed = models.DateTimeField()
    cloudSaveStatus = models.BooleanField()


class User(models.Model):
    username = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    firstname = models.CharField(max_length=200)
    lastname = models.CharField(max_length=200)
    birthday = models.DateTimeField()
    vac = models.BooleanField()
    level = models.IntegerField()
    library_id = models.OneToOneField(Library, on_delete=models.CASCADE)


class Achievement(models.Model):
    name = models.CharField(max_length=200, default="Undefined")
    description = models.CharField(max_length=200, null=True)
    gameID = models.IntegerField()


class Wishlist(models.Model):
    gameID = models.IntegerField()


class Review(models.Model):
    heading = models.CharField(max_length=200, default="Undefined")
    text = models.CharField(max_length=200, null=True)
    rating = models.SmallIntegerField()
    userID = models.IntegerField()


class AchievedBy(models.Model):
    userID = models.CharField(max_length=200)
    achievementID = models.IntegerField()
    timestamp = models.DateTimeField()
