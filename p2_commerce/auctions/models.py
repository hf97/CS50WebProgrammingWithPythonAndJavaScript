from django.contrib.auth.models import AbstractUser
from django.db import models

from datetime import datetime

class User(AbstractUser):
    pass

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    text = models.CharField(max_length=1000)
    # TODO ver se blank esta bem
    date = models.DateTimeField(default=datetime.now, blank=True)

class Category(models.Model):
    name = models.CharField(max_length=64)

class Listing(models.Model):
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=1000)
    startingBid = models.FloatField()
    image = models.URLField()
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.PROTECT, default=1)

class Bid(models.Model):
    bidder = models.ForeignKey(User, on_delete=models.PROTECT)
    listing = models.ForeignKey(Listing, on_delete=models.PROTECT)
    price = models.FloatField()
