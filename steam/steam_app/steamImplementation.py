from .models import *


class Steam:

    @staticmethod
    def release_new_game(game, achievements):
        Game.objects.model.save(game, force_insert=True)
        for achievement in achievements:
            Achievement.objects.model.save(achievement)

    @staticmethod
    def create_new_user(user):
        db_object = User.objects.create(user)

