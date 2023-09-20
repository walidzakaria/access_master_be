from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import Q


# Create your models here.
class User(AbstractUser):
    email = models.EmailField(verbose_name='email',
                              max_length=255, unique=True)
    branch = models.ForeignKey('entry.branch', on_delete=models.CASCADE, null=True, blank=True)
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name', ]
    USERNAME_FIELD = 'email'

    def get_username(self):
        return self.email

    def get_type(self):
        groups = self.groups.first()
        if groups:
            return groups.name
        return 'no group'


class LogInfo(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    code = models.CharField(max_length=40)
    device = models.CharField(max_length=20)
    device_family = models.CharField(max_length=20)
    browser = models.CharField(max_length=40)
    operating_system = models.CharField(max_length=40)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)
    ip = models.CharField(max_length=20, default='', null=True, blank=True)

    def __str__(self):
        return f'{self.device}-{self.device_family}: {self.browser}-{self.operating_system}: {self.ip}'

    def user_info(self):
        return f'{self.device}-{self.device_family}: {self.browser}-{self.operating_system}: {self.ip}'
