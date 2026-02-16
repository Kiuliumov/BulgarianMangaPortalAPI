from django.contrib.auth.models import AbstractUser
from django.db import models


class Account(AbstractUser):
    display_name = models.CharField(max_length=50, unique=True, blank=True, null=True)
    slug = models.SlugField(unique=True, blank=True)

    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)
    banner = models.ImageField(upload_to="banners/", blank=True, null=True)

    friends = models.ManyToManyField("self", symmetrical=True, blank=True)
    blocked_users = models.ManyToManyField("self", symmetrical=False, blank=True, related_name="blocked_by")

    reputation = models.IntegerField(default=0)

    posts_count = models.PositiveIntegerField(default=0)
    comments_count = models.PositiveIntegerField(default=0)

    is_verified = models.BooleanField(default=False)
    is_private = models.BooleanField(default=False)

    last_seen = models.DateTimeField(blank=True, null=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.display_name or self.username
