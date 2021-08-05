import json

from django.views    import View
from django.http     import JsonResponse

from products.models import Category, SubCategory

class NavigatorView(View):
    def get(self, request):
        categories = Category.objects.all()
        category_lst = []
        for category in categories:
            sub_categories = category.subcategory_set.all()
            sub_category_lst = []
            for sub_category in sub_categories:
                sub_category_lst.append({
                    'sub_category_id'   : sub_category.id,
                    'name' : sub_category.name
                })
            category_lst.append({
                'category_id'  : category.id,
                'name': category.name,
                'sub_categories' : sub_category_lst
            })
        return JsonResponse({"categories":category_lst}, status=200)

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