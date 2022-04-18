from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Post(models.Model):
    owner = models.ForeignKey("User", on_delete=models.CASCADE, related_name="posts")
    title = models.CharField(max_length=255)
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default=0)

    def __str__(self):
        return f"On {self.timestamp} {self.owner.username} posted: \"{self.title[:40]}\""

    def serialize(self):
        return {
            "id": self.id,
            "owner_id": self.owner.id,
            "owner_name": self.owner.username,
            "title": self.title,
            "text": self.text,
            "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p"),
            "likes": self.likes
        }