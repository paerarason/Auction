from django.urls import include,path
from .import views
from rest_framework.authtoken.views import obtain_auth_token
urlpatterns=[
    path('auction/',views.Auction_list),
    path('auction/<int:pk>',views.Auction_detail),

    path('user/',views.user_list),
    path('user/<int:pk>',views.user_detail),
  
    path('bids',views.bid_list),
    #path('bids/<int:pk>',views.bid_list),
    path('api-token-auth/',obtain_auth_token),
]