import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):

    id = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        primary_key=True,
        editable=False
    )

    def get_full_name(self):
        """
        Return the fullname.
        """
        return self.profile.full_name

    def get_short_name(self):
        """Return the short name for the user."""
        return self.profile.short_name
