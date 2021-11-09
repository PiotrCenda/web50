from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.utils.timezone import now
from django.core.validators import MinValueValidator


class Auction(models.Model):
    CATEGORIES = [
        ('B', 'book'),
        ('M', 'music'),
        ('F', 'film'),
        ('O', 'other')
    ]

    title = models.CharField(max_length=64)
    description = models.CharField(max_length=300)
    image_url = models.CharField(max_length=300, blank=True, default=None)
    category = models.CharField(max_length=30, choices=CATEGORIES)
    starting_bid = models.PositiveIntegerField(default=10, validators=[MinValueValidator(1, message="must be greater than 0")])
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="auctions")
    active = models.BooleanField(default=True, blank=False)

    def __str__(self):
        return f"{self.title} auction by {self.owner}"


class User(AbstractUser):
    watchlist = models.ManyToManyField(Auction, blank=True, related_name="watched_by")


class Bid(models.Model):
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name="auction_bids")
    value = models.PositiveIntegerField(validators=[MinValueValidator(1, message="must be greater than 0")])
    bid_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="bid_authors")
    datetime = models.DateTimeField(default=now, editable=False)

    def __str__(self):
        return f"{self.value} bid by {self.bid_user}"


class Comment(models.Model):
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name="comments")
    text = models.CharField(max_length=300)
    comment_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="comment_authors")
    datetime = models.DateTimeField(default=now, editable=False)

    def __str__(self):
        return f"{self.comment_user} comment on {self.auction}"
