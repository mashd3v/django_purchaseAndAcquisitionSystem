from django.db import models
from django.contrib.auth.models import User
from django_userforeignkey.models.fields import UserForeignKey

class ModelClass(models.Model):
    status = models.BooleanField(default=True)
    creationDate = models.DateTimeField(auto_now_add=True)
    modificationDate = models.DateTimeField(auto_now=True)
    userCreator = models.ForeignKey(User, on_delete=models.CASCADE)
    userModifier = models.IntegerField(blank=True, null=True)

    class Meta:
        abstract = True

class ModelClass2(models.Model):
    status = models.BooleanField(default=True)
    creationDate = models.DateTimeField(auto_now_add=True)
    modificationDate = models.DateTimeField(auto_now=True)
    userCreator = UserForeignKey(auto_user_add=True, related_name='+')
    userModifier = UserForeignKey(auto_user=True, related_name='+')

    class Meta:
        abstract = True
