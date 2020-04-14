import factory
from django.db import IntegrityError
from django.db.models.signals import post_save
from django.forms.models import model_to_dict
from django.test import TestCase

from .factories import UserFactory
from .factories import UserProfileFactory
from apps.users.models import User
from apps.users.models import UserProfile


class TestCaseUser(TestCase):
    def test_create(self):
        """
        Test the creation of a User model using a factory
        """
        UserFactory.create()
        self.assertEqual(User.objects.count(), 1)

    def test_create_batch(self):
        """
        Test the creation of 5 User models using a factory
        """
        users = UserFactory.create_batch(5)
        self.assertEqual(User.objects.count(), 5)
        self.assertEqual(len(users), 5)

    def test_attribute_count(self):
        """
        Test that all attributes of User server are counted.
        It will count the primary key and all editable attributes.
        This test should break if a new attribute is added.
        """
        user = UserFactory.create()
        user_dict = model_to_dict(user)
        self.assertEqual(len(user_dict.keys()), 15)

    def test_attribute_content(self):
        """
        Test that all attributes of User server have content.
        This test will break if an attributes name is changed.
        """
        user = UserFactory.create()
        self.assertIsNotNone(user.id)
        self.assertIsNotNone(user.password)
        self.assertIsNotNone(user.last_login)
        self.assertIsNotNone(user.is_superuser)
        self.assertIsNotNone(user.username)
        self.assertIsNotNone(user.first_name)
        self.assertIsNotNone(user.last_name)
        self.assertIsNotNone(user.name)
        self.assertIsNotNone(user.email)
        self.assertIsNotNone(user.is_staff)
        self.assertIsNotNone(user.is_active)
        self.assertIsNotNone(user.date_joined)
        self.assertIsNotNone(user.is_trusty)

    def test_username_is_unique(self):
        """
        Tests attribute username of model User to see if the unique constraint works.
        This test should break if the unique attribute is changed.
        """
        user = UserFactory.create()
        user_02 = UserFactory.create()
        user_02.username = user.username
        try:
            user_02.save()
            self.fail("Test should have raised and integrity error")
        except IntegrityError as e:
            self.assertEqual(
                str(e), "UNIQUE constraint failed: users_user.username"
            )


class TestCaseUserProfile(TestCase):
    def test_create(self):
        """
        Test the creation of a UserProfile model using a factory
        """

        UserFactory.create()
        # user_profile = UserProfileFactory.create()
        self.assertEqual(UserProfile.objects.count(), 1)

    def test_create_batch(self):
        """
        Test the creation of 5 UserProfile models using a factory
        """
        users = UserFactory.create_batch(5)
        # user_profiles = UserProfileFactory.create_batch(5)
        self.assertEqual(UserProfile.objects.count(), 5)
        self.assertEqual(len(users), 5)

    def test_attribute_count(self):
        """
        Test that all attributes of UserProfile server are counted.
        It will count the primary key and all editable attributes.
        This test should break if a new attribute is added.
        """

        user = UserFactory.create()
        print("USERS=", User.objects.count())
        print("PROFI=", UserProfile.objects.count())

        # user_profile = UserProfileFactory.create()
        user_profile = user.profile
        user_profile_dict = model_to_dict(user_profile)
        # self.assertEqual(len(user_profile_dict.keys()), 14)
        self.assertEqual(len(user_profile_dict.keys()), 12)

    def test_attribute_content(self):
        """
        Test that all attributes of UserProfile server have content.
        This test will break if an attributes name is changed.
        """
        with factory.django.mute_signals(post_save):
            user = UserFactory.create()
        user_profile = UserProfileFactory.create(user=user)
        # user_profile = user.profile
        user_profile_dict = model_to_dict(user_profile)
        for i, key in enumerate(user_profile_dict.keys()):
            print("%s [%s]=[%s]" % (i, key, getattr(user_profile, key)))

        self.assertIsNotNone(user_profile.id)
        self.assertIsNotNone(user_profile.created)
        self.assertIsNotNone(user_profile.modified)
        self.assertIsNotNone(user_profile.user)
        self.assertIsNotNone(user_profile.photo)
        self.assertIsNotNone(user_profile.phone)
        self.assertIsNotNone(user_profile.bio)
        self.assertIsNotNone(user_profile.organization)
        self.assertIsNotNone(user_profile.website)
        self.assertIsNotNone(user_profile.facebook)
        self.assertIsNotNone(user_profile.instagram)
        self.assertIsNotNone(user_profile.birthday)
        self.assertIsNotNone(user_profile.city)
        self.assertIsNotNone(user_profile.country)

    def test_user_is_unique(self):
        """
        Tests attribute user of model UserProfile to see if the unique constraint works.
        This test should break if the unique attribute is changed.
        """

        user = UserFactory.create()
        user_02 = UserFactory.create()

        user_profile = user.profile
        user_profile_02 = user_02.profile

        # user_profile = UserProfileFactory.create()
        # user_profile_02 = UserProfileFactory.create()
        user_profile_02.user = user_profile.user
        try:
            user_profile_02.save()
            self.fail("Test should have raised and integrity error")
        except IntegrityError as e:
            print("IT SHOULD BE=[%s]" % e)
            self.assertEqual(
                str(e), "UNIQUE constraint failed: users_userprofile.user_id"
            )
