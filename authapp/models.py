from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import Q


# Create your models here.
class User(AbstractUser):
    email = models.EmailField(verbose_name='email',
                              max_length=255, unique=True)
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name', ]
    USERNAME_FIELD = 'email'

    def get_username(self):
        return self.email

    def get_type(self):
        groups = self.groups.first()
        if groups:
            return groups.name
        return 'employee'
        
    
    def get_colleagues(self):
        """
        Retrieves all employee colleagues
        """
        # @TODO: fix error here when team leader is invoked
        employees = EmployeePosition.objects.filter(
            last_position=True,
        ).filter(
            Q(team__team_leader_one__login=self) |
            Q(team__team_leader_two__login=self)
        ).all().values_list('employee__login__id', flat=True)
        result = list(employees)
        result.append(self.id)
        return result
    
    def get_teams(self):
        """
        Retrieves all employee teams
        """
        teams = EmployeePosition.objects.filter(
            last_position=True
        ).filter(
            Q(team__team_leader_one__login=self) |
            Q(team__team_leader_two__login=self) |
            Q(employee__login=self)
        ).all().values_list('team__id', flat=True)
        return list(teams)
    


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
