from django.test import TestCase
from .models import *
import json

from .steamImplementation import Steam

ALL_FIXTURES = ["games.json"]


# Create your tests here.
class GameTestCase(TestCase):
    fixtures = ALL_FIXTURES

    def test_create_game(self):
        diablo = Game.objects.get(pk=1)
        self.assertEquals(diablo.name, "Diablo IV")

    def test_create_user(self):
        user = User.objects.get(pk=1)
        self.assertEquals(user.firstname, "Schpadel")

    def test_publish_new_game(self):
        game = Game(publisher="Giants Software", size=30, developer="Giants Software", franchise="Simulation",
                    description="Farm some shit", release_date="2023-05-23", supported_languages="EN",
                    supported_platforms="PC,Switch", rating=69, usk=0, genre="Simulation", price=44.99,
                    name="Landwirtschafts Simulator 23")
        game.pk = 999
        achievements = list()
        achievements.append(Achievement(game_id=999, description="Help your neighbor", name="Friendly Dude"))
        achievements.append(Achievement(game_id=999, description="Earn some cash", name="Lets gooooo"))
        Steam.release_new_game(game, achievements)
        game_from_db = Game.objects.get(pk=999)

        # Check if game was saved to db correctly
        self.assertEquals(game_from_db, game)

        achievements_for_game = list(Achievement.objects.filter(game_id=999))
        self.assertEquals(achievements_for_game.pop(), achievements.pop())
