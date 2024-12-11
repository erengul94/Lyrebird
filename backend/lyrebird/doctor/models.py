from django.db import models
from django.contrib.auth.models import User
from django.db import models
# Create your models here.
from client.models import Client

class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="doctor_profile", null=True)
    address = models.CharField(max_length=100, null=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"