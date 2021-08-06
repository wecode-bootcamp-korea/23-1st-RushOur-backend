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
        
        if category_id:
            product_filter.add(Q(sub_category__category=category_id), Q.AND)

        if subcategory_id:
            product_filter.add(Q(sub_category=subcategory_id), Q.AND)
             
        products = Product.objects.filter(product_filter)
        
        if tags:
            for tag in tags:
                products = products.filter(tags__name=tag)

        if sort:
            products = products.annotate(price=Min('option__price')).order_by(sort)

        products_lst = [{
                'id'        : product.id,
                'name'      : product.name,
                'price'     : product.option_set.all()[0].price,
                'thumbnail' : product.thumbnail_image_url,
                'tags'      : [tag.name for tag in product.tags.all()]
            }for product in products]

        return JsonResponse({'products':products_lst}, status=200)