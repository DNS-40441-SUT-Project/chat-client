from django.db import models
from .base import BaseModel


class BaseMessage(BaseModel):
    sender = models.CharField(max_length=256, db_index=True)

    # must be encrypted with secret_key
    content = models.TextField()

    class Meta:
        abstract = True


class GroupMessage(BaseMessage):
    group = models.CharField(max_length=256, db_index=True)


class UserMessage(BaseMessage):
    receiver = models.CharField(max_length=256, db_index=True)
