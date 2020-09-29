from decimal import Decimal
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from django.db import models


class User(AbstractUser):
    pass

class Category(models.Model):
    name = models.CharField(max_length=32)

    def __str__(self):
        return f'{self.name}'

class Listing(models.Model):
    user = models.ForeignKey('User', default=None, on_delete=models.CASCADE)
    name = models.CharField(max_length=64)
    price = models.DecimalField(max_digits=6, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    description = models.TextField(max_length=200)
    active = models.BooleanField(default=True)
    category = models.ForeignKey('Category', default=None, on_delete=models.CASCADE)
    image = models.URLField(max_length=765, blank=True, null=True)
    bids = models.ManyToManyField('Bid', blank=True, related_name='listing_bids')

    def __str__(self):
        return f'{self.name}'

class Comment(models.Model):
    user = models.ForeignKey('User', default=None, on_delete=models.CASCADE)
    listing = models.ForeignKey('Listing', default=None, on_delete=models.CASCADE)
    content = models.CharField(max_length=200)
    
    def __str__(self):
        return f'{self.user}: {self.content}'

class Bid(models.Model):
    user = models.ForeignKey('User', default=None, on_delete=models.CASCADE)
    value = models.DecimalField(max_digits=6, decimal_places=2 )

    def __str__(self):
        return f'$ {self.value} by {self.user}'

class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None )
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, default=None )

    def __str__(self):
        return f'{self.listing}'
