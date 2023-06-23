from .models import *


class Steam:

    @staticmethod
    def release_new_game(game, achievements):
        db_object = Game.objects.model.save(game, force_insert=True)
        #for achievement in achievements:
        #    Achievement.objects.create(achievement)

    @staticmethod
    def create_new_user(user):
        db_object = User.objects.create(user)

