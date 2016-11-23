from django.test import TestCase
from django.test import Client
from videos.models import Video
from users.models import User
from django.contrib.auth.models import User
from django.db import models

class view_tests(TestCase):
	def test_view_error_404_random_string(self):
		client = Client()
		response = client.get('/alkfddaklfjh')
		self.assertEqual(response.status_code, 404)

	def test_view_code_200(self):
		client = Client()
		response = client.get('/')
		self.assertEqual(response.status_code, 302)

	def test_permision_delete(self):
		userpep = User.objects.create_user(username="pepito", email="pepito@hotmail.com", password="123")
		userjuan = User.objects.create_user(username="juansito", email="juansito@yahoo.com", password="456")
		userpep.save()
		userjuan.save()

		video = Video(title="pepito bailando full HD 1 link MEGA", description="Video gracioso de pepito bailando, manito arriba si te gusto", author=userjuan)
		video.save()

		clientpepito = Client()
		clientpepito.login(username=userpep, password="123")

		response = clientpepito.get("/video/"+str(video.id)+"/delete/")

		self.assertEqual(response.status_code, 404)

	def test_permision_delete_no_loggin(self):
		useromar = User.objects.create_user(username="omar", email="omar@hotmail.com", password="123")
		userfer = User.objects.create_user(username="fer", email="ferchu@yahoo.com", password="456")
		useromar.save()
		userfer.save()

		video = Video(title="omar escabiado", description="omar muy escabiado", author=useromar)
		video.save()

		clientomar = Client()

		response = clientomar.get("/video/"+str(video.id)+"/delete/")

		self.assertEqual(response.status_code, 302)

	def test_upload_invalid(self):

		useroscar = User.objects.create_user(username="oscar", email="oscar@hotmail.com", password="123")
		
		useroscar.save()

		clienteoscar = Client()
		clienteoscar.login(username="oscar", password="123")

		fp = open("test.txt", "a+")

		response = clienteoscar.post('/video/upload/', {'author': 'oscar', 'title': 'videotest','description' : 'testeando', 'file' :fp})
		videos = Video.objects.filter(title="videotest")
		self.assertEqual(0, Video.objects.filter(title="videotest").count())

	def test_upload_valid(self):
		userflor = User.objects.create_user(username="flor", email="flor@hotmail.com", password="123")
		
		userflor.save()

		clientflor = Client()
		clientflor.login(username="flor", password="123")

		fp = open('test_media/bestanimal.mp4')


		response = clientflor.post('/video/upload/', {'author': 'flor', 'title': 'videotestcabra','description' : 'testeando', 'file' :fp})
		self.assertEqual(1, Video.objects.filter(title="videotestcabra").count())
