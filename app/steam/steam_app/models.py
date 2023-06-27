from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import MinValueValidator


class Game(models.Model):
    name = models.CharField(max_length=200)
    genre = models.CharField(max_length=200)
    publisher = models.CharField(max_length=200)
    developer = models.CharField(max_length=200)
    franchise = models.CharField(max_length=200)
    price = models.DecimalField(decimal_places=2, max_digits=10, validators=[MinValueValidator(0.0)])
    size = models.DecimalField(decimal_places=2, max_digits=100, validators=[MinValueValidator(0.0)])
    rating = models.SmallIntegerField()
    release_date = models.DateField("date released")
    usk = models.SmallIntegerField(validators=[MinValueValidator(0)])
    supported_platforms = models.CharField(max_length=200, default="PC")
    supported_languages = models.CharField(max_length=200)
    description = models.CharField(max_length=20_000)
    version = models.CharField(max_length=20)

    def release_new_game(self, achievements):
        Game.objects.model.save(self, force_insert=True)
        for achievement in achievements:
            Achievement.objects.model.save(achievement)

    def update_game_version(self, new_version):
        self.version = new_version
        Game.objects.model.save(self)

    class Meta:
        # rating can only be between 0% and 100%
        constraints = [models.CheckConstraint(name="correct_rating", check=models.Q(rating__range=(0, 100)), ),
                       models.UniqueConstraint(fields=["name"], name="unique_game_name")]


class SteamUser(models.Model):
    username = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    firstname = models.CharField(max_length=200)
    lastname = models.CharField(max_length=200)
    birthday = models.DateField()
    vac = models.BooleanField()
    level = models.PositiveIntegerField(validators=[MinValueValidator(1)])

    class Meta:
        constraints = [models.UniqueConstraint(fields=['username'], name='unique_username')]


class Wishlist(models.Model):
    wished_Games = models.ManyToManyField(Game)
    user = models.OneToOneField(SteamUser, on_delete=models.CASCADE, null=False)

    # create a new wishlist if a user is created!
    @receiver(post_save, sender=SteamUser)
    def create_wishlist(sender, instance, created, **kwargs):
        if created:
            Wishlist.objects.create(user=instance)


class Library(models.Model):
    games_in_lib = models.ManyToManyField(Game, through="steam_app.GamesInLibrary")
    user = models.OneToOneField(SteamUser, on_delete=models.CASCADE, null=False)

    @receiver(post_save, sender=SteamUser)
    def create_library(sender, instance, created, **kwargs):
        if created:
            Library.objects.create(user=instance)


class GamesInLibrary(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    library = models.ForeignKey(Library, on_delete=models.CASCADE)
    timePlayed = models.DurationField(validators=[MinValueValidator(0)])
    lastPlayed = models.DateTimeField()
    cloudSaveStatus = models.BooleanField()


class Achievement(models.Model):
    name = models.CharField(max_length=200, default="Undefined")
    description = models.CharField(max_length=200, null=True)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)


class Review(models.Model):
    heading = models.CharField(max_length=200, default="Undefined")
    text = models.CharField(max_length=200, null=True)
    rating = models.SmallIntegerField()
    user = models.ForeignKey(SteamUser, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)


class AchievedBy(models.Model):
    user = models.ForeignKey(SteamUser, on_delete=models.CASCADE)
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE)
    timestamp = models.DateTimeField()

    class Meta:
        constraints = [models.UniqueConstraint(fields=['user', 'achievement'], name='unique_achievement_unlock')]
