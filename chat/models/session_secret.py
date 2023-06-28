from django.db import models

from ..models.base import BaseModel


class SessionSecret(BaseModel):
    user = models.ForeignKey(
        to='chat.User',
        on_delete=models.CASCADE,
        related_name='%(class)s_secrets',
    )

    # encrypted with password of user and with this secret he can encrypt it.
    # we can use Fernet for this or use django secret system
    # key for end to end encryption
    secret_key = models.TextField()

    class Meta:
        abstract = True


# it is just for save who has the secrets for our chat session
class UserSecret(SessionSecret):
    # we may have not its own password
    other_user = models.ForeignKey(
        to='chat.User',
        on_delete=models.CASCADE,
        related_name='other_user_secrets',
    )

    class Meta:
        unique_together = (
            'user',
            'other_user',
        )


# after anyone add somebody to group we need to send secret_key for that user.
class GroupSecret(SessionSecret):
    group = models.ForeignKey(
        to='chat.Group',
        on_delete=models.CASCADE,
        related_name='group_secrets',
    )

    class Meta:
        unique_together = (
            'user',
            'group',
        )
