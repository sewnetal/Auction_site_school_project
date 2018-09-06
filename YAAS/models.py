from django.db import models


class Auction(models.Model):
    seller = models.CharField(max_length=20)
    title = models.CharField(max_length=20)
    description = models.TextField()
    min_price = models.FloatField(max_length=20)
    starting_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(null=True)
    status = models.CharField(max_length=20,null=True)
    category = models.CharField(max_length=20)
    current_bidder = models.CharField(max_length=20,null=True)
    auction_winner = models.CharField(max_length=20,null=True)

    def __unicode__(self):
        return self.seller





