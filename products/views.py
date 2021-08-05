import json

from django.views    import View
from django.http     import JsonResponse

from products.models import Category 

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