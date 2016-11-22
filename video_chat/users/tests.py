from django.test import TestCase

from users.models import User, UserProfile, FriendRequest
from django.core.urlresolvers import reverse
from django.db.models import Q


# Create your tests here.
def create_user(name):
    user = User.objects.create(username=name, email=name+"@gmail.com", password="secret")
    UserProfile.objects.create(user=user)
    return user

def create_request(sender, receiver):
    FriendRequest.objects.create(sender=sender, receiver=receiver)

def create_friendship(user1, user2):
    user1.userprofile.friends.add(user2.userprofile)

class FriendRequestViewTest(TestCase):
    def test_send_new_request(self):
        alice = create_user("Alice")
        bob = create_user("Bob")  
        self.client.force_login(alice)

        self.client.post(reverse('users:send_request'), {'friend_pk': bob.pk})

        self.assertEqual(FriendRequest.objects.filter(Q(sender=alice, receiver=bob) | 
            Q(sender = bob, receiver = alice)).count(), 1)

    def test_send_request_twice(self):
        alice = create_user("Alice")
        bob = create_user("Bob")  
        self.client.force_login(alice)
        create_request(alice, bob);

        self.client.post(reverse('users:send_request'), {'friend_pk': bob.pk})

        self.assertEqual(FriendRequest.objects.filter(Q(sender=alice, receiver=bob) | 
            Q(sender = bob, receiver = alice)).count(), 1)

    def test_send_request_after_receive(self):
        alice = create_user("Alice")
        bob = create_user("Bob")  
        self.client.force_login(alice)
        create_request(bob, alice);

        self.client.post(reverse('users:send_request'), {'friend_pk': bob.pk})

        self.assertEqual(FriendRequest.objects.filter(Q(sender=alice, receiver=bob) | 
            Q(sender = bob, receiver = alice)).count(), 1)

    def test_send_request_to_friend(self):
        alice = create_user("Alice")
        bob = create_user("Bob")  
        create_friendship(alice, bob)

        self.client.force_login(alice)
        self.client.post(reverse('users:send_request'), {'friend_pk': bob.pk})

        self.assertEqual(FriendRequest.objects.filter(Q(sender=alice, receiver=bob) | 
            Q(sender = bob, receiver = alice)).count(), 0)


