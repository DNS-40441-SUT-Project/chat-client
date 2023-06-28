from django.db import models
from .base import BaseModel


class BaseMessage(BaseModel):
    sender = models.ForeignKey(
        to='chat.User',
        on_delete=models.CASCADE,
        related_name='%(class)s_sent_messages',
    )

    # must be encrypted with secret_key
    content = models.TextField()

    class Meta:
        abstract = True


class GroupMessage(BaseMessage):
    group = models.ForeignKey(
        to='chat.Group',
        on_delete=models.CASCADE,
        related_name='messages',
    )


class UserMessage(BaseMessage):
    receiver = models.ForeignKey(
        to='chat.User',
        on_delete=models.CASCADE,
        related_name='received_messages',
    )
