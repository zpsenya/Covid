from django.db import models


class Clients(models.Model):
    name = models.TextField(max_length=80)
    surname = models.TextField(max_length=80)
    id_doctor = models.IntegerField()
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Time of create")
    time_update = models.DateTimeField(auto_now=True, verbose_name="Time of update")
    time_of_analyse = models.DateTimeField(verbose_name="Time of analyse")
    email = models.EmailField(auto_created=f'{name}_{surname}@gmail.com')
    is_corona = models.BooleanField(default=False)

    def __repr__(self):
        return f'Name is {self.name}'


class Users(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.TextField(max_length=80)
    surname = models.TextField(max_length=80)

    def __repr__(self):
        return f'Name is {self.name}'



