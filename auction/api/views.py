from django.shortcuts import render
from .models import *
import datetime
from rest_framework.decorators import api_view
from .serializers import *
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from .bidding import proces,result
from datetime import datetime
@api_view(["GET","POST"])
@permission_classes([IsAuthenticated])
def Auction_list(request):
   auction=Auction.objects.all()
   print(auction)
   if request.user.groups.filter(name='user').exists():
     if request.method=="GET":
        auction=Auction.objects.filter(status='ONGOING')
        print(auction) 
        serializer_item=AuctionSerializer(auction,many=True)
        return Response(serializer_item.data,status=status.HTTP_200_OK)     
   if request.user.groups.filter(name='Admin').exists():
     if request.method=="GET":
        serializer_item=AuctionSerializer(auction,many=True)
        return Response(serializer_item.data,status=status.HTTP_200_OK)
     if request.method=="POST":
        serializers_item=AuctionSerializer(data=request.data)
        if serializers_item.is_valid():
           serializers_item.save()
           return Response(serializers_item.data,status=status.HTTP_200_OK)
   return Response(status=status.HTTP_403_FORBIDDEN)



@api_view(["GET"])
@permission_classes([IsAuthenticated])
def Auction_detail(request,pk):
    try:
        auction=Auction.objects.get(id=pk)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method=="GET":
       serializer_item=AuctionSerializer(auction)
       return Response(serializer_item.data,status=status.HTTP_200_OK)
    if request.user.groups.filter(name='Admin').exists():
        if request.method=="PUT":
           data=request.data
           serializers_item=AuctionSerializer(auction,data=request.data)
           if serializers_item.is_valid():
             serializers_item.save()
             return Response(serializers_item.data,status=status.HTTP_200_OK) 
        elif request.method=="PATCH":
           data=request.data
           serializers_item=CurrentUserSerializer(auction,data=request.data,many=True)
           if serializers_item.is_valid():
             serializers_item.save()
             return Response(serializers_item.data,status=status.HTTP_200_OK)
        elif request.method=="DELETE":
           auction.delete()
           return Response(status=status.HTTP_200_OK)
    return Response(status=status.HTTP_403_FORBIDDEN)


@api_view(["GET","POST"])
@permission_classes([IsAuthenticated])
def user_list(request):
     if request.user.groups.filter(name='Admin').exists():
        if request.method=="GET":
          users=User.objects.all()
          print(users)
          serializers_item=CurrentUserSerializer(users,many=True)
          return Response(serializers_item.data,status=status.HTTP_200_OK)
        elif request.method=="POST":
          serializers_item=CurrentUserSerializer(data=request.data)
          if serializers_item.is_valid():
             serializers_item.save()
             return Response(serializers_item.data,status=status.HTTP_200_OK)  
     return Response(status=status.HTTP_403_FORBIDDEN)
     
@api_view(["GET","PUT","PATCH","DELETE"])
@permission_classes([IsAuthenticated])
def user_detail(request,pk):
     if request.user.groups.filter(name='Admin').exists():
        try:
           users=User.objects.get(id=pk)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if request.method=="GET":         
           serializers_item=CurrentUserSerializer(users)
           return Response(serializers_item.data,status=status.HTTP_200_OK)
        elif request.method=="PUT":
           data=request.data
           serializers_item=CurrentUserSerializer(users,data=data)
           if serializers_item.is_valid():
             serializers_item.save()
             return Response(serializers_item.data,status=status.HTTP_200_OK) 
        elif request.method=="PATCH":
           data=request.data
           serializers_item=CurrentUserSerializer(users,data=data,partial=True)
           print(serializers_item)
           if serializers_item.is_valid():
             serializers_item.save()
             return Response(serializers_item.data,status=status.HTTP_200_OK)
        elif request.method=="DELETE":
           users.delete()
           return Response(status=status.HTTP_200_OK)
     return Response(status=status.HTTP_403_FORBIDDEN)




@api_view(["GET","POST"])
@permission_classes([IsAuthenticated])
def bid_list(request):
   if request.user.groups.filter(name='Admin').exists():
        if request.method=="GET":
          bids=Bid.objects.all()
          bids=proces(bids)
          serializers_item=BidsSerializer(bids,many=True)
          return Response(serializers_item.data,status=status.HTTP_200_OK)
   if request.user.groups.filter(name='user').exists():
        if request.method=="POST":
           serializers_item=BidsSerializer(data=request.data)
           if serializers_item.is_valid():
             serializers_item.save()
             if  datetime.now()>serializers_item.auction.end_time:         
               now=result(Bid.objects.get(auction=request.data['auction']))
               serializers_item.auction.price_end=now.price
               serializers_item.auction.winner=now.bidder
             return Response(serializers_item.data,status=status.HTTP_200_OK)
        if request.method=="GET":
           bids=Bid.objects.all()
           print(bids)
           bids=proces(bids)
           serializers_item=BidsSerializer(bids,many=True)
           return Response(serializers_item.data,status=status.HTTP_200_OK)
   return Response(status=status.HTTP_403_FORBIDDEN)
