from django.urls import path

from banners.views import BannersView

urlpatterns = [
   path('', BannersView.as_view())
]