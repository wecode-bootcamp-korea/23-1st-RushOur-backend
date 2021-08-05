from django.urls import path

from products.views import CategoryView, NavigatorView, SubCategoryView

urlpatterns = [
    path('/navigator', NavigatorView.as_view()),
    path('/category/<int:category_id>', CategoryView.as_view()),
    path('/subcategory/<int:subcategory_id>', SubCategoryView.as_view()),
]