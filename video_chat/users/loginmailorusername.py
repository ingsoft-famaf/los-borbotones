from django.conf import settings
from django.contrib.auth.models import User

def authenticatemailoruser(self, username, password):
    if '@' in username:
        kwargs = {'email': username}
    else:
        kwargs = {'username': username}
    try:
        user = User.objects.get(**kwargs)
        if user.check_password(password):
            return user
    except User.DoesNotExist:
        return None
