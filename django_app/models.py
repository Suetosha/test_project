from django.db import models


class Menu(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)


class Item(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', null=True, on_delete=models.CASCADE)

    objects = models.Manager()
