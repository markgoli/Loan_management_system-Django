from django.db import models
from django.contrib.auth.models import User

class UserDetail(models.Model):
    user_gender = [
        ('male','Male'),
        ('female','Female')
    ]
    first_name = models.CharField(max_length=20, null=True, blank=True)
    last_name = models.CharField(max_length=20, null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    gender = models.CharField(max_length=20, choices=user_gender, null=True, blank=True)
    is_admin = models.BooleanField(default=False, null=True, blank=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        db_table =  'user_details'