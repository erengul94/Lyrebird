from django.db import models
from client.models import Client
# Create your models here.


class Patient(models.Model):
    first_name = models.CharField(max_length=100, null=True)
    last_name = models.CharField(max_length=100, null=True)
    address = models.CharField(max_length=100, null=True)
    email = models.EmailField(max_length=100, null=True)
    phone_number = models.CharField(max_length=100, null=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} "


    def toDict(self):
        return {
            "user_id": self.id,
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "phone_number":  self.phone_number
        }