import json

from django.views     import View
from django.http      import JsonResponse
from django.db.models import Min

from products.models  import Category, SubCategory, Product

class NavigatorView(View):
    def get(self, request):
        categories = Category.objects.all()
        navigator_lst = [{
                'category_id'   : category.id,
                'name'          : category.name,
                'products_count': Product.objects.filter(sub_category__category=category).count(),
                'subcategories' : [{
                    'subcategory_id': subcategory.id,
                    'name'          : subcategory.name,
                    'products_count': subcategory.product_set.count()
                } for subcategory in category.subcategory_set.all()],
            } for category in categories ]
        return JsonResponse({"navigators":navigator_lst}, status=200)

class CategoryView(View):
    def get(self, request, category_id):
        if not Category.objects.filter(id=category_id).exists():
            return JsonResponse({"MESSAGE":"INVALID_ID"}, status=404)

        category = Category.objects.get(id=category_id)
        category_des = {
            'name'       : category.name,
            'image_url'  : category.image_url,
            'description': category.description
        }
        return JsonResponse({'category':category_des}, status=200)


class SubCategoryView(View):
    def get(self, request, subcategory_id):
        if not SubCategory.objects.filter(id=subcategory_id).exists():
            return JsonResponse({"MESSAGE":"INVALID_ID"}, status=404)

        subcategory = SubCategory.objects.get(id=subcategory_id)
        sub_category_des = {
            'name'       : subcategory.name,
            'image_url'  : subcategory.image_url,
            'description': subcategory.description
        }
        return JsonResponse({'subcategory':sub_category_des}, status=200)
