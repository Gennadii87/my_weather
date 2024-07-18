from django.test import TestCase, Client
from .models import CitySearch


class CitySearchTests(TestCase):

    def setUp(self):
        self.client = Client()

    def test_city_search_creation(self):
        self.client.post('/', {'city': 'London'})
        self.assertEqual(CitySearch.objects.count(), 1)
        self.assertEqual(CitySearch.objects.first().city_name, 'London')

    def test_history_view(self):
        session = self.client.session
        session['last_city'] = 'London'
        session.save()
        response = self.client.get('/last/')
        self.assertEqual(response.json()['last_city'], 'London')
