from django.urls import path
from wishlists.models import User,Product, Wishlist

urlpatterns = [ 
	path ('/like', Wishlist.as_view())
] 
