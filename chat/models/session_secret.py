from django.db import models

from ..models.base import BaseModel


class SessionSecret(BaseModel):
    secret_key = models.TextField()

    class Meta:
        abstract = True


class UserSecret(SessionSecret):
    other_user = models.CharField(max_length=256, unique=True)


class GroupSecret(SessionSecret):
    group = models.CharField(max_length=256, unique=True)
