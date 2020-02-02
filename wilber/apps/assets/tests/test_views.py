from django.test import TestCase
from django.urls import reverse





class TestCalls(TestCase):
    def test_call_view_denies_anonymous(self):
        pass
        #response = self.client.get(reverse('home'), follow=True)
        #self.assertRedirects(response, '/login/')
        #response = self.client.post(reverse('home'), follow=True)
        #self.assertRedirects(response, '/login/')
