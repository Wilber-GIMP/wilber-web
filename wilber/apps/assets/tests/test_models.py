from django.test import TestCase
from django.forms.models import model_to_dict
from django.db import IntegrityError
from django.conf import settings


from .factories import AssetFactory
from .factories import LikeFactory

from assets.models import Asset
from assets.models import Like

class TestCaseAsset(TestCase):

    def test_create(self):
        """
        Test the creation of a Asset model using a factory
        """
        asset = AssetFactory.create()
        self.assertEqual(Asset.objects.count(), 1)

    def test_create_batch(self):
        """
        Test the creation of 5 Asset models using a factory
        """
        assets = AssetFactory.create_batch(5)
        self.assertEqual(Asset.objects.count(), 5)
        self.assertEqual(len(assets), 5)


    def test_attribute_count(self):
        """
        Test that all attributes of Asset server are counted. It will count the primary key and all editable attributes.
        This test should break if a new attribute is added.
        """
        asset = AssetFactory.create()
        asset_dict = model_to_dict(asset)
        #self.assertEqual(len(asset_dict.keys()), 17)
        self.assertEqual(len(asset_dict.keys()), 9)



    def test_attribute_content(self):
        """
        Test that all attributes of Asset server have content. This test will break if an attributes name is changed.
        """
        asset = AssetFactory.create()
        self.assertIsNotNone(asset.id)
        self.assertIsNotNone(asset.created)
        self.assertIsNotNone(asset.modified)
        self.assertIsNotNone(asset.owner)
        self.assertIsNotNone(asset.category)
        self.assertIsNotNone(asset.name)
        self.assertIsNotNone(asset.slug)
        self.assertIsNotNone(asset.description)
        self.assertIsNotNone(asset.source)
        self.assertIsNotNone(asset.file)
        self.assertIsNotNone(asset.filesize)
        self.assertIsNotNone(asset.image)
        self.assertIsNotNone(asset.num_likes)
        self.assertIsNotNone(asset.num_downloads)
        self.assertIsNotNone(asset.num_views)
        self.assertIsNotNone(asset.created_at)
        self.assertIsNotNone(asset.updated_at)


    def test_slug_is_unique(self):
        """
        Tests attribute slug of model Asset to see if the unique constraint works.
        This test should break if the unique attribute is changed.
        Autoslug auto changes slug fields to ensure uniqueness
        """
        asset = AssetFactory.create()
        asset_02 = AssetFactory.create()
        asset_02.slug = asset.slug
        asset_02.save()
        
        self.assertNotEqual(asset.slug, asset_02.slug)
        


class TestCaseLike(TestCase):

    def test_create(self):
        """
        Test the creation of a Like model using a factory
        """
        like = LikeFactory.create()
        self.assertEqual(Like.objects.count(), 1)

    def test_create_batch(self):
        """
        Test the creation of 5 Like models using a factory
        """
        likes = LikeFactory.create_batch(5)
        self.assertEqual(Like.objects.count(), 5)
        self.assertEqual(len(likes), 5)


    def test_attribute_count(self):
        """
        Test that all attributes of Like server are counted. It will count the primary key and all editable attributes.
        This test should break if a new attribute is added.
        """
        like = LikeFactory.create()
        like_dict = model_to_dict(like)
        self.assertEqual(len(like_dict.keys()), 3)



    def test_attribute_content(self):
        """
        Test that all attributes of Like server have content. This test will break if an attributes name is changed.
        """
        like = LikeFactory.create()
        self.assertIsNotNone(like.id)
        self.assertIsNotNone(like.user)
        self.assertIsNotNone(like.asset)
        self.assertIsNotNone(like.timestamp)
