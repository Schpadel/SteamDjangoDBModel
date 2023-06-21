from django.test import TestCase
from .models import *

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

