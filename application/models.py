import django.contrib.auth.forms
from django.db import models


class Client(models.Model):
    name = models.TextField(max_length=80)
    surname = models.TextField(max_length=80)
    doctor_id = models.ForeignKey(django.contrib.auth.forms.UserModel, on_delete=models.CASCADE)
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Time of create")
    time_update = models.DateTimeField(auto_now=True, verbose_name="Time of update")
    time_of_analyse = models.DateTimeField(verbose_name="Time of analyse")
    email = models.EmailField()
    is_corona = models.BooleanField(default=False)

