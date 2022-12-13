from rest_framework import serializers
from .models import Auction
from django.contrib.auth.models import User
class CurrentUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'id']

class AuctionSerializer(serializers.ModelSerializer):
    user=CurrentUserSerializer(read_only=True)
    class Meta:
        model=Auction
        fields=['id','user','item_name','price_from','end_time','start_time','price_end','winner','status']

class BidsSerializer(serializers.ModelSerializer):
   bidder=CurrentUserSerializer(read_only=True)
   auction=AuctionSerializer(read_only=True)
   class Meta:
       fields=['bidder','auction','price']
