import json

from django.views     import View
from django.http      import JsonResponse
from django.db.models import Min

from products.models import Category, SubCategory, Product, Tag

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

class ProductsView(View):
    def get(self, request):
        category_id = request.GET.get('category')
        subcategory_id = request.GET.get('subcategory')
        tag_name = request.GET.get('tag')
        sort = request.GET.get('sort')

        if category_id:
            if not Category.objects.filter(id=category_id).exists():
                return JsonResponse({"MESSAGE":"INVALID_ID"}, status=404)
            products = Product.objects.filter(sub_category__category=category_id)

        if subcategory_id:    
            if not SubCategory.objects.filter(id=subcategory_id).exists():
                return JsonResponse({"MESSAGE":"INVALID_ID"}, status=404)
            products = Product.objects.filter(sub_category=subcategory_id)
        
        if tag_name:
            if not Tag.objects.filter(name=tag_name).exists():
                return JsonResponse({"MESSAGE":"NOT_FOUND_TAG"}, status=404)
            products = Product.objects.filter(tags__name=tag_name)
        
        products_lst = []
        if sort:
            products = products.annotate(price=Min('option__price')).order_by(sort)

        for product in products:
            tag_lst = []
            tags = product.tags.all()
            for tag in tags:
                tag_lst.append(tag.name) 
            products_lst.append({
                'id'        : product.id,
                'name'      : product.name,
                'price'     : product.option_set.all()[0].price,
                'thumbnail' : product.thumbnail_image_url,
                'tags'      : tag_lst
            })
        return JsonResponse({'products':products_lst}, status=200)