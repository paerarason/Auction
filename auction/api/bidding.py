from .models import Auction,Bid
def heapify(bids,n,i):
     left=2*i+1
     right=2*i+2
     largest=i
     if bids[largest].price<bids[left].price and left<n:
        largest=left 
     if bids[largest].price < bids[right].price and right<n:
        largest=right
     if largest!=i:
       bids[i],bids[largest]=bids[i],bids[largest]
       heapify(bids,n,largest)
def proces(bids):
    for i in range(len(bids)//2,0,-1):
        heapify(bids,len(bids),i)
    return bids
def result(bids):
   return proces(bids)