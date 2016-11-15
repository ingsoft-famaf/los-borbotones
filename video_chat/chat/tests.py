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
    content_text = '<p>Hola</p>'

    def setUp(self):
        user = User.objects.create_user(self.fake_username, self.fake_mail,self.fake_pass)
        self.user = UserProfile(user = user)
        self.user.save()
        self.video = Video(title = "TITULO", description = "DESCRIPCION", autor = user)
        self.video.save()
        self.chat_room = ChatRoom(video = self.video)
        self.chat_room.save()

    def test_message_get_escaped(self):
        c = Client()
        c.login(username = self.fake_username, password = self.fake_pass)
        c.post('/chat/chat/', {'content_text':self.content_text, 'chat_id':self.chat_room.id}, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        response = c.get('/chat/messages/'+str(self.video.id), HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        correct_response = "<p>"+escape(self.user.user.username)+": "+escape(self.content_text)+"</p>"
        self.assertEqual(response.content, correct_response)
