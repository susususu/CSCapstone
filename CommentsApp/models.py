from django.db import models

# Create your models here.

from GroupsApp.models import Group
from AuthenticationApp.models import MyUser

class Comment(models.Model):
    time = models.DateTimeField(auto_now=True)
    comment = models.CharField(max_length=500)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, null=True)