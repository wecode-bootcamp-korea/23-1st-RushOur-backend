from django.urls import path

from carts.views import CartView, CartsView

urlpatterns = [
    path('/<int:cart_id>', CartView.as_view()),
    path('', CartsView.as_view()),
]