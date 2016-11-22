from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.utils.html import escape

from models import ChatRoom, Message
from users.models import UserProfile
from videos.models import Video
# Create your tests here.

class ViewsTestCase(TestCase):
    user = None
    chat_room = None
    video = None
    fake_username = 'pedro'
    fake_mail = 'pedro@mail.com'
    fake_pass = 'password'

    def setUp(self):
        user = User.objects.create_user(self.fake_username, self.fake_mail,self.fake_pass)
        self.user = UserProfile(user = user)
        self.user.save()
        self.video = Video(title = "TITULO", description = "DESCRIPCION", author = user)
        self.video.save()
        self.chat_room = self.user.chatroom_set.create(video=self.video)

    def test_message_get_escaped(self):
        content_text = '<p>Hola</p>'
        c = Client()
        c.login(username = self.fake_username, password = self.fake_pass)
        c.post('/chat/chat/', {'content_text':content_text, 'chat_id':self.chat_room.id}, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        response = c.get('/chat/messages/'+str(self.chat_room.pk), HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        correct_response = "<p>"+escape(self.user.user.username)+": "+escape(content_text)+"</p>"
        self.assertEqual(response.content, correct_response)

    def test_long_message(self):
        content_text = 'A'*10000
        c = Client()
        c.login(username = self.fake_username, password = self.fake_pass)
        response = c.post('/chat/chat/', {'content_text':content_text, 'chat_id':self.chat_room.id}, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)

    def test_anon_user_create_message(self):
        content_text = 'Hola'
        c = Client()
        response = c.post('/chat/chat/', {'content_text':content_text, 'chat_id':self.chat_room.id}, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 302)

    def test_anon_user_reads_messages(self):
        c = Client()
        response = c.get('/chat/messages/'+str(self.video.id), HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 302)
