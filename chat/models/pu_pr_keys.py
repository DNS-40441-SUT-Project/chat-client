from django.db import models

from ..models.base import BaseModel


class PuPrKey(BaseModel):
    user = models.ForeignKey(
        to='chat.User',
        on_delete=models.CASCADE,
        related_name='pu_pr_keys',
        unique=True,
    )

    # everyone can see this
    public_key = models.TextField()

    # encrypted with password of user and with this secret he can encrypt it.
    # we can use Fernet for this or use django secret system
    private_key = models.TextField(null=True)
