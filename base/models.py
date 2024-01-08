# models.py

from django.contrib.auth.models import AbstractUser
from django.db import models
from .managers import CustomUserManager

class User(AbstractUser):
    username = models.CharField(max_length=255, unique=True)
    fullname = models.CharField(max_length=255, default="")
    email = models.EmailField(unique=True)
    mobile_number = models.CharField(max_length=15)
    collector = models.BooleanField(default=False)
    # Add or change related_name for groups and user_permissions
    groups = models.ManyToManyField('auth.Group', related_name='base_user_groups', blank=True)
    user_permissions = models.ManyToManyField('auth.Permission', related_name='base_user_permissions', blank=True)
    
    objects = CustomUserManager()

# models.py

class ClientRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    location = models.CharField(max_length=255)
    type_of_waste = models.CharField(max_length=50, choices=[
        ('Plastic', 'Plastic'),
        ('Paper', 'Paper'),
        ('Glass', 'Glass'),
        ('Metal', 'Metal'),
        ('Wet waste', 'Wet waste'),
        ('Dry waste', 'Dry waste'),
        ('Others', 'Others'),
        # Add more choices as needed
    ])
    timestamp = models.DateTimeField(auto_now_add=True)
    alloted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.id} - {self.user} - {self.user.mobile_number} - {self.location}"


class Allocation(models.Model):
    collector = models.ForeignKey(User, on_delete=models.CASCADE)
    client_request = models.ForeignKey('ClientRequest', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)


class CollectorReport(models.Model):
    collector = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    client_request = models.OneToOneField('ClientRequest', on_delete=models.CASCADE, default=None, unique=True)
    material = models.TextField(default=None)
    quantity = models.IntegerField(default=None)
    detail = models.TextField(default=None)
    finalprice = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    confirmation_from_client = models.BooleanField(default=False)
    transaction_completed = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.collector.username} - Report for Request {self.client_request.id}"

class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

