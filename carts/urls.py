from django.urls import path

from carts.views import CartsView

urlpatterns = [
    path('', CartsView.as_view())
]