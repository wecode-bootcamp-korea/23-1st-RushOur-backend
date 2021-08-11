from django.urls import path
from wishlists.views import WishlistView

urlpatterns = [ 
	path ('/like', WishlistView.as_view())
] 
