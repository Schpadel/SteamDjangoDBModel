from django.db import models


# Create your models here.
class Game(models.Model):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key, value in kwargs.items():
            setattr(self, key, value)

    name = models.CharField(max_length=200)
    genre = models.CharField(max_length=200)
    publisher = models.CharField(max_length=200)
    developer = models.CharField(max_length=200)
    franchise = models.CharField(max_length=200)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    size = models.DecimalField(decimal_places=2, max_digits=100)
    rating = models.SmallIntegerField()
    release_date = models.DateField("date released")
    usk = models.SmallIntegerField()
    supported_platforms = models.CharField(max_length=200, default="PC")
    supported_languages = models.CharField(max_length=200)
    description = models.CharField(max_length=20_000)

    def release_new_game(self, achievements):
        Game.objects.model.save(self, force_insert=True)
        for achievement in achievements:
            Achievement.objects.model.save(achievement)

    class Meta:
        constraints = [models.CheckConstraint(name="Test Int Constraint", check=models.Q(rating__range=(0, 100)), )]


class Library(models.Model):
    timePlayed = models.DurationField()
    lastPlayed = models.DateTimeField()
    cloudSaveStatus = models.BooleanField()
    game = models.ManyToManyField(Game)


class Wishlist(models.Model):
    gameID = models.ManyToManyField(Game)


class User(models.Model):
    username = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    firstname = models.CharField(max_length=200)
    lastname = models.CharField(max_length=200)
    birthday = models.DateField()
    vac = models.BooleanField()
    level = models.IntegerField()
    library = models.OneToOneField(Library, on_delete=models.CASCADE)
    wishList = models.OneToOneField(Wishlist, on_delete=models.CASCADE)

    # get all games for this user
    def get_all_games(self):
        return self.library.objects.all()


class Achievement(models.Model):
    name = models.CharField(max_length=200, default="Undefined")
    description = models.CharField(max_length=200, null=True)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)


class Review(models.Model):
    heading = models.CharField(max_length=200, default="Undefined")
    text = models.CharField(max_length=200, null=True)
    rating = models.SmallIntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)


class AchievedBy(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE)
    timestamp = models.DateTimeField()
