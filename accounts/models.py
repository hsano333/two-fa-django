from django.db import models
from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser,
    PermissionsMixin,
    Group,
    Permission,
)


import pyotp
from django.contrib.auth import password_validation


# Create your models here.
class FtUser(AbstractBaseUser, PermissionsMixin):

    groups = models.ManyToManyField(Group, related_name="ft_user_groups")
    user_permissions = models.ManyToManyField(
        Permission, related_name="ft_user_permissions"
    )

    username = models.CharField(verbose_name="ユーザー名", max_length=32, unique=False)
    email = models.CharField(verbose_name="email", max_length=256, unique=True)
    first_name = models.CharField(
        verbose_name="姓",
        max_length=150,
    )
    last_name = models.CharField(
        verbose_name="名",
        max_length=150,
    )
    app_secret = models.CharField(
        verbose_name="App鍵",
        max_length=32,
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"username={self.username}, email={self.email}"

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    objects = BaseUserManager()


class FtTmpUser(AbstractBaseUser, PermissionsMixin):
    groups = models.ManyToManyField(Group, related_name="ft_tmpuser_groups")
    user_permissions = models.ManyToManyField(
        Permission, related_name="ft_tmpuser_permissions"
    )

    username = models.CharField(verbose_name="ユーザー名", max_length=32, unique=False)
    email = models.CharField(verbose_name="email", max_length=256, unique=True)
    first_name = models.CharField(
        verbose_name="姓",
        max_length=150,
    )
    last_name = models.CharField(
        verbose_name="名",
        max_length=150,
    )
    app_secret = models.CharField(
        verbose_name="App鍵",
        max_length=32,
        null=True,
        blank=True,
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]
    objects = BaseUserManager()

    def save(self, *args, **kwargs):
        # 一度だけ実行するように
        if not self.app_secret:
            totp = pyotp.TOTP(pyotp.random_base32())
            secret = totp.secret
            self.app_secret = secret
        super().save(*args, **kwargs)
        if self._password is not None:
            password_validation.password_changed(self._password, self)
            self._password = None
