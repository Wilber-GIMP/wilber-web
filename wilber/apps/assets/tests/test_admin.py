from django.contrib.admin.sites import AdminSite
from django.contrib.messages.storage.fallback import FallbackStorage
from django.core.files.base import ContentFile
from django.core.files.base import File
from django.test import RequestFactory
from django.test import TestCase
from django.urls import reverse

from apps.assets.admin import AssetAdmin
from apps.assets.models import Asset
from apps.users.models import User


class MockSuperUser:
    def has_perm(self, perm):
        return True


request_factory = RequestFactory()
request = request_factory.get("/admin")
request.user = MockSuperUser()

# If you need to test something using messages
setattr(request, "session", "session")
messages = FallbackStorage(request)
setattr(request, "_messages", messages)

TEST_CATEGORY = "_TEST_CATEGORY"


class AssetAdminTest(TestCase):
    def setUp(self):
        site = AdminSite()
        self.admin = AssetAdmin(Asset, site)

        self.username = "john"
        self.password = "goldenstandard"
        self.user = User.objects.create_superuser(
            username=self.username,
            email="jlennon2@beatles.com",
            password=self.password,
        )

        self.asset = Asset.objects.create(
            name="Test Asset Admin 10", owner=self.user, category=TEST_CATEGORY
        )
        self.asset2 = Asset.objects.create(
            name="Test Asset Admin 20", owner=self.user, category=TEST_CATEGORY
        )

        self.file = ContentFile(b"model_id\n1\n2\n" * 1000)

    def test_delete_model(self):
        obj = Asset.objects.get(pk=1)
        self.admin.delete_model(request, obj)

        deleted = Asset.objects.filter(pk=1).first()
        self.assertEqual(deleted, None)

    def test_recalculate_likes(self):
        data = {
            "action": "recalculate_likes",
            "_selected_action": [self.asset.id, self.asset2.id],
        }
        change_url = reverse("admin:assets_asset_changelist")

        # print(dir(self.admin.get_actions(request)))
        # self.client.login(username=self.username, password=self.password)
        self.client.login(username=self.username, password=self.password)
        response = self.client.post(change_url, data, follow=True)
        self.assertEqual(response.status_code, 200)

    def test_filesize(self):
        asset = Asset.objects.get(id=1)
        f = File(open("test/package_file.zip", "rb"))
        asset.file.save("test_xyz_filename.zip", f)

        self.assertEqual(asset.get_filesize(), 567418)

        url = reverse("admin:assets_asset_changelist")
        self.client.login(username=self.username, password=self.password)
        self.client.get(url, follow=True)

    def test_file_upload(self):
        # each admin url consits of the following three things
        # the app name, the name of the model and the name of the view
        url = reverse("admin:assets_asset_change", kwargs={"object_id": 1})
        self.client.login(username=self.username, password=self.password)
        # resp = self.client.get(url, follow=True)
        resp = self.client.post(
            url, {"form_filefield": self.file}, follow=True
        )

        # Here you'll want to do extra assertions, ie are you
        # saving the file in a model, streaming something back in
        # streamingresponse or doing something else.
        self.assertEqual(resp.status_code, 200)

        url = reverse("admin:assets_asset_changelist")
        resp = self.client.get(url, follow=True)

        self.assertEqual(resp.status_code, 200)
