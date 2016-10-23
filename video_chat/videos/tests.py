from django.test import TestCase
from django.test import Client
from .models import Video

class view_tests(TestCase):
	def test_view_error_404_random_string(self):
		client = Client()
		response = client.get('/alkfddaklfjh')
		self.assertEqual(response.status_code, 404)

	def test_view_code_200(self):
		client = Client()
		response = client.get('/')
		self.assertEqual(response.status_code, 200)
