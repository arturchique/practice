from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=60)
    info = models.CharField(max_length=150)
    location = models.ForeignKey('Address', on_delete=models.SET_NULL, null=True)


class Address(models.Model):
    name = models.CharField(max_length=60)