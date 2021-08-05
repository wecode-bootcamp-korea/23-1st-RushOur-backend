from django.urls import path
from carts.views import CartView,CartDetailView

urlpatterns = [ 
	path ('/cart', CartView.as_view()),
	path ('/cart/<int:cart_id>', CartDetailView.as_view())
] 
