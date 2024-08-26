from django.contrib.auth.backends import ModelBackend
from .models import FtTmpUser


class FtTmpUserBackend(ModelBackend):
    def authenticate(self, request, email=None, password=None):
        if email is None or password is None:
            return
        user = FtTmpUser.objects.get(email=email)
        pwd_valid = user.check_password(password)
        if pwd_valid:
            return user
        return None

    def get_user(self, user_id):
        try:
            return FtTmpUser.objects.get(pk=user_id)
        except FtTmpUser.DoesNotExist:
            return None
