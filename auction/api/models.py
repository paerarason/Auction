from django.db import models
from django.contrib.auth.models import User
class Auction(models.Model):
    status_choice=[("COMPLETED","completed"),("ONGOING","ongoing"),(" yet to be  STARTED","yet to start")]
    start_time=models.DateTimeField()
    item_name=models.CharField(max_length=255)
    end_time=models.DateTimeField()
    price_from=models.IntegerField()
    price_end=models.IntegerField(null=True,blank=True)
    winner=models.ForeignKey(User,on_delete=models.SET_NULL,related_name="winner",null=True,blank=True)
    status=models.CharField(choices=status_choice,default="yet to start",max_length=30)
    def __str__(self) -> str:
        return  self.item_name
    
class Bid(models.Model):
    bidder=models.ForeignKey(User,on_delete=models.CASCADE,related_name="bidder")
    auction=models.ForeignKey(Auction,on_delete=models.CASCADE,related_name="Auction_BID")
    price=models.IntegerField()
    time=models.TimeField(auto_now_add=True)