from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

class User(AbstractUser):
    pass

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    listing = models.ForeignKey("Listing", on_delete=models.PROTECT, default=0)
    text = models.CharField(max_length=1000)
    # TODO ver se blank esta bem
    date = models.DateTimeField(default=timezone.now, blank=True)

class Category(models.Model):
    name = models.CharField(max_length=64)
    def __str__(self):
        return self.name

class Listing(models.Model):
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=1000)
    startingBid = models.FloatField()
    image = models.URLField()
    date = models.DateTimeField(default=timezone.now, blank=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.PROTECT, default=1)
    latestBid = models.ForeignKey("Bid", on_delete=models.PROTECT, related_name="ltBid", blank=True, null=True)

class Bid(models.Model):
    bidder = models.ForeignKey(User, on_delete=models.PROTECT)
    listing = models.ForeignKey(Listing, on_delete=models.PROTECT)
    date = models.DateTimeField(default=timezone.now, blank=True)
    price = models.FloatField()

class WatchList(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    listings = models.ManyToManyField(Listing, related_name="watch", null=True, blank=True)
