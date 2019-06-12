import os
from django.test import TestCase

from django.test import TestCase
from django.urls import reverse

from django.core.files.base import ContentFile
from django.core.files.base import File

from .models import Asset
from .models import Like
from users.models import User



class AssetTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='john',
                                 email='jlennon@beatles.com',
                                 password='glass onion')
                                 
        self.user2 = User.objects.create_user(username='john2',
                                 email='jlennon2@beatles.com',
                                 password='glass onion')
                                 
        self.asset = Asset.objects.create(name='Test Asset 1', owner=self.user)

    def test_simple_asset(self):
        asset = Asset.objects.get(id=1)
        expected_object_name = str(asset)
        self.assertEquals(expected_object_name, 'Test Asset 1')
        
        self.assertEquals(asset.get_absolute_url(), '/asset/1')
        
    def test_asset_with_created_file(self):
        asset = Asset.objects.get(id=1)
        asset.file.save('test_filename', ContentFile('Test File'))
        
        self.assertEqual(asset.get_filesize(), 9)
        
    def test_asset_with_existing_file(self):
        asset = Asset.objects.get(id=1)
        
        f = File(open('static/imgs/01.jpg', 'rb'))
        asset.file.save('test_filename', f)
        
        self.assertEqual(asset.get_filesize(), 85718)
        
        asset.image.save('image-name', File(open('static/imgs/02.jpg', 'rb')))
        
    
    def test_like(self):
        self.assertEqual(self.asset.num_likes, 0)
        like, created = self.asset.do_like(self.user)
        self.assertEqual(self.asset.num_likes, 1)
        self.assertEqual(str(like), 'john likes Test Asset 1')
        
        self.asset.do_like(self.user)
        self.assertEqual(self.asset.num_likes, 1)
        
        self.asset.do_like(self.user2)
        self.assertEqual(self.asset.num_likes, 2)
        self.asset.unlike(self.user)
        self.asset.refresh_from_db()
        self.assertEqual(self.asset.num_likes, 1)
        self.asset.unlike(self.user2)
        self.asset.refresh_from_db()
        self.assertEqual(self.asset.num_likes, 0)
        
        self.asset.unlike(self.user2)
        self.asset.refresh_from_db()
        self.assertEqual(self.asset.num_likes, 0)
        

    def test_asset_list_view(self):
        response = self.client.get(reverse('asset:list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Asset 1')
        self.assertTemplateUsed(response, 'assets/asset_list.html')
        
