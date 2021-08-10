"""rushour URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include

from products.views import CategoryView, NavigatorView, SubCategoriesView, SubCategoryView

urlpatterns = [
    path('products', include('products.urls')),
    path('users', include('users.urls')),
    path('navigator', NavigatorView.as_view()),
    path('category/<int:category_id>', CategoryView.as_view()),
    path('subcategory/<int:subcategory_id>', SubCategoryView.as_view()),
    path('subcategory', SubCategoriesView.as_view()),
    path('banners', include('banners.urls')),
]
