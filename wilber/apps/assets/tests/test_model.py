from django.test import TestCase
from django.urls import reverse

from django.core.files.base import ContentFile
from django.core.files.base import File
import random
from ..models import Asset
from users.models import User

TEMP_FILENAME = 'test_filenameX.zip'
TEST_CATEGORY = '_TEST_CATEGORY'
from zipfile import BadZipFile

class AssetTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='john',
                                 email='jlennon@beatles.com',
                                 password='glass onion')
                                 
        self.user2 = User.objects.create_user(username='john2',
                                 email='jlennon2@beatles.com',
                                 password='glass onion')

        n1 = random.randint(0, 100)
        n2 = random.randint(0, 100)


        name = "Test XYZ Model"
        self.name1 = '%s 19' % name
        self.name2 = '%s %d' % (name, n2)

        self.asset = Asset.objects.create(name=self.name1, owner=self.user, category=TEST_CATEGORY)
        self.asset2 = Asset.objects.create(name=self.name2, owner=self.user, category=TEST_CATEGORY)

    def test_simple_asset(self):
        asset = Asset.objects.get(id=1)
        expected_object_name = str(asset)
        self.assertEqual(expected_object_name, self.name1)
        
        #self.assertEquals(asset.get_absolute_url(), '/asset/1')
        
    def test_asset_with_created_file(self):
        asset = Asset.objects.get(id=1)
        with self.assertRaises(BadZipFile):
            asset.file.save(TEMP_FILENAME, ContentFile('Test File'))
        
        self.assertEqual(asset.get_filesize(), 9)
        
    def test_asset_with_existing_file(self):
        asset = Asset.objects.get(id=1)
        
        f = File(open('test/package_file.zip', 'rb'))
        asset.file.save(TEMP_FILENAME, f)
        
        #self.assertEqual(asset.get_filesize(), 567418)
        self.assertEqual(asset.get_filesize(), 566943)

        asset.image.save('image-name.jpg', File(open('test/image.jpg', 'rb')))
        
    
    def test_like(self):
        self.assertEqual(self.asset.num_likes, 0)
        like, created = self.asset.do_like(self.user)
        self.assertEqual(self.asset.num_likes, 1)
        self.assertEqual(str(like), 'john likes Test XYZ Model 19')
        
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
        self.assertContains(response, 'Test XYZ Model 19')
        self.assertTemplateUsed(response, 'assets/asset_list.html')


    def tearDown(self):
        print("tearDown")
        self.asset.delete()
        self.asset2.delete()