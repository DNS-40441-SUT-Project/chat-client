from functools import cached_property

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from django.db import models

from ..models.base import BaseModel


class SessionSecret(BaseModel):
    secret_key = models.TextField()

    class Meta:
        abstract = True

    @cached_property
    def pub_key(self):
        return serialization.load_pem_public_key(
            self.secret_key.encode(),
            backend=default_backend()
        )


class UserSecret(SessionSecret):
    other_user = models.CharField(max_length=256, unique=True)


class GroupSecret(SessionSecret):
    group = models.CharField(max_length=256, unique=True)
