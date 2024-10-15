import datetime

from django.db import models


class AppStors(models.Model):
    name = models.CharField(max_length=100)
    year = models.DateField()
    users = models.IntegerField()

    def __str__(self):
        return self.name

    @property
    def age_stor(self):
        return datetime.datetime.now().year - self.year

class App(models.Model):
    name = models.CharField(max_length=100)
    year = models.DateField()
    direction = models.TextField(max_length=400)
    stor = models.ForeignKey(AppStors, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name


