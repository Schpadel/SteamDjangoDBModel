from django.test import TestCase
from .models import Game


# Create your tests here.
class GameTestCase(TestCase):
    def setUp(self):
        Game.objects.create(name='DiabloIV', release_date='01.01.2000')
