import json

from django.views    import View
from django.http     import JsonResponse

from products.models  import Category, SubCategory, Product, Tag
from django.db.models import Min, Q

class ProductsView(View):
    def get(self, request):
        category_id    = request.GET.get('category') 
        subcategory_id = request.GET.get('subcategory')
        tags           = request.GET.getlist('tag')
        sort           = request.GET.get('sort')

        product_filter = Q()
        
        sort_by = {
            'name'      : 'name',
            'low_price' : 'price',
            'high_price': '-price'
        }
        
        if category_id:
            product_filter.add(Q(sub_category__category=category_id), Q.AND)

        if subcategory_id:
            product_filter.add(Q(sub_category=subcategory_id), Q.AND)
             
        products = Product.objects.filter(product_filter).annotate(price=Min('option__price')).order_by(sort_by.get(sort, "name"))
        
        if tags:
            for tag in tags:
                products = products.filter(tags__name=tag)

        products_lst = [{
                'id'        : product.id,
                'name'      : product.name,
                'price'     : product.price,
                'thumbnail' : product.thumbnail_image_url,
                'tags'      : [tag.name for tag in product.tags.all()]
            } for product in products]

        return JsonResponse({'products':products_lst}, status=200)

class ProductView(View):
    def get(self, request, product_id):
        if not Product.objects.filter(id=product_id).exists():
            return JsonResponse({"MESSAGE":"INVALID_ID"}, status=404)

        product      = Product.objects.get(id=product_id)
        product_data = {
            'id'           : product.id,
            'name'         : product.name,
            'thumbnail'    : product.thumbnail_image_url,
            'options'      : [{
                'size'  : option.size,
                'price' : option.price
            } for option in product.option_set.all()],
            'tags'         : [tag.name for tag in product.tags.all()],
            'detail_img'   : [image.image_url for image in product.productdetailimage_set.all()]
        }
        return JsonResponse({"data":product_data}, status=200)

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
            'id'         : category.id,
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
            'id'         : subcategory.id,
            'name'       : subcategory.name,
            'image_url'  : subcategory.image_url,
            'description': subcategory.description
        }
        return JsonResponse({'subcategory':sub_category_des}, status=200)

class SubCategoriesView(View):
    def get(self, request):           
        subcategories = [{
            'id'         : subcategory.id,
            'name'       : subcategory.name,
            'image_url'  : subcategory.image_url,
            'description': subcategory.description
            } for subcategory in SubCategory.objects.all()]
        return JsonResponse({"subcategories":subcategories}, status=200)
