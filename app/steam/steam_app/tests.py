from django.db import IntegrityError, transaction
from django.test import TestCase
from django.utils import timezone

from .models import *

ALL_FIXTURES = ["games.json", "users.json", "achievedBy.json", "achievements.json", "libraries.json",
                "reviews.json", "wishlist.json", "library_game_relation.json", "wishlist_wished_Games_relation.json"]


# Create your tests here.
class GameTestCase(TestCase):
    fixtures = ALL_FIXTURES

    def test_create_game(self):
        diablo = Game.objects.get(pk=1)
        self.assertEquals(diablo.name, "Diablo IV")

    def test_create_user(self):
        user = SteamUser.objects.get(pk=1)
        self.assertEquals(user.username, "Schpadel")

    def test_update_game_version(self):
        game_to_update = Game.objects.get(pk=1)
        game_to_update.update_game_version("2.0")

        game_from_db = Game.objects.get(pk=1)
        self.assertEquals(game_from_db.version, "2.0")

    def test_all_games_in_library(self):
        all_games = SteamUser.objects.get(username="Schpadel").library.games.all()

        # test if all games which are assigned in fixture are there
        owned_games_pk = [1, 3, 4, 6]
        for owned_game_pk in owned_games_pk:
            self.assertTrue(Game.objects.get(pk=owned_game_pk) in all_games)

    def test_publish_new_game(self):
        game = Game(publisher="Giants Software", size=30, developer="Giants Software", franchise="Simulation",
                    description="Farm some shit", release_date="2023-05-23", supported_languages="EN",
                    supported_platforms="PC,Switch", rating=69, usk=0, genre="Simulation", price=44.99,
                    name="Landwirtschafts Simulator 23")
        game.pk = 999
        achievements = list()
        achievements.append(Achievement(game_id=999, description="Help your neighbor", name="Friendly Dude"))
        achievements.append(Achievement(game_id=999, description="Earn some cash", name="Lets gooooo"))
        game.release_new_game(achievements)
        game_from_db = Game.objects.get(pk=999)

        # Check if game was saved to db correctly
        self.assertEquals(game_from_db, game)

        achievements_from_db = list(Achievement.objects.filter(game_id=999))
        self.assertEquals(achievements_from_db, achievements)

    def test_delete_player(self):
        user_to_delete = SteamUser.objects.filter(username="Schpadel")
        deleted_user_id = user_to_delete.first().id
        deleted_user_username = user_to_delete.first().username
        user_to_delete.delete()

        # check if user has been deleted in all relevant tables
        self.assertNotIn(deleted_user_username, SteamUser.objects.values_list("username", flat=True))
        self.assertNotIn(deleted_user_id, Library.objects.values_list("pk", flat=True))
        self.assertNotIn(deleted_user_id, Review.objects.values_list("user_id", flat=True))
        self.assertNotIn(deleted_user_id, AchievedBy.objects.values_list("user_id", flat=True))
        self.assertNotIn(deleted_user_id, Wishlist.objects.values_list("user_id", flat=True))

    def test_update_price_of_game(self):
        game_to_update = Game.objects.get(pk=1)
        game_to_update.price = 200
        game_to_update.save()

        self.assertEquals(200, Game.objects.get(pk=1).price)

    def test_unlock_achievements(self):
        user_to_unlock_achievement = SteamUser.objects.get(pk=1)
        achievement_to_unlock = Achievement.objects.get(pk=2)

        AchievedBy.objects.create(achievement=achievement_to_unlock, timestamp=timezone.now(),
                                  user=user_to_unlock_achievement)

        self.assertEquals(achievement_to_unlock, user_to_unlock_achievement.achievedby_set.filter(
            achievement=achievement_to_unlock).first().achievement)
        self.assertEquals(user_to_unlock_achievement,
                          achievement_to_unlock.achievedby_set.filter(achievement=achievement_to_unlock).first().user)

    def test_unlock_same_achievement_twice(self):
        user_to_unlock_achievement = SteamUser.objects.get(pk=1)
        achievement_to_unlock = Achievement.objects.get(pk=2)

        AchievedBy.objects.create(achievement=achievement_to_unlock, timestamp=timezone.now(),
                                  user=user_to_unlock_achievement)

        with transaction.atomic():  # atomic to make sure self.assertRaises works correctly
            with self.assertRaises(IntegrityError):
                AchievedBy.objects.create(achievement=achievement_to_unlock, timestamp=timezone.now(),
                                          user=user_to_unlock_achievement)

        self.assertEquals(achievement_to_unlock, user_to_unlock_achievement.achievedby_set.filter(
            achievement=achievement_to_unlock).first().achievement)
        self.assertEquals(user_to_unlock_achievement, achievement_to_unlock.achievedby_set.filter(
            achievement=achievement_to_unlock).first().user)

    def test_delete_review(self):
        user_who_wants_to_delete = SteamUser.objects.get(pk=1)

        count_of_reviews = user_who_wants_to_delete.review_set.count()
        user_who_wants_to_delete.review_set.all().first().delete()

        self.assertEquals(count_of_reviews - 1, user_who_wants_to_delete.review_set.count())

    def test_add_games_to_wishlist(self):
        user = SteamUser.objects.get(pk=2)

        count_of_games_on_wishlist = user.wishlist.wished_Games.count()
        user.wishlist.wished_Games.add(Game.objects.get(pk=4))

        self.assertEquals(count_of_games_on_wishlist + 1, user.wishlist.wished_Games.count())

        # wishlist of random other user not affected
        self.assertEquals(1, SteamUser.objects.get(pk=3).wishlist.wished_Games.count())

    def test_remove_games_from_wishlist(self):
        user = SteamUser.objects.get(pk=3)

        count_of_games_on_wishlist = user.wishlist.wished_Games.count()
        user.wishlist.wished_Games.remove(Game.objects.get(pk=5))

        self.assertEquals(count_of_games_on_wishlist - 1, user.wishlist.wished_Games.count())
