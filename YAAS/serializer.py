__author__ = 'sewnet'
from rest_framework import serializers
from YAAS.models import Auction

class AuctionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Auction
        fields =('title','description','min_price','category','end_date','status')

class BidSerializer(serializers.ModelSerializer):

    class Meta:
        model = Auction
        fields = ('min_price',)