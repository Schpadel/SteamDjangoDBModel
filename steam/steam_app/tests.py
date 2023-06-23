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
        achievements = list()
        # achievements.append(Achievement(gameID_id=1, ))
        Steam.release_new_game(game, achievements)


