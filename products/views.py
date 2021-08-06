import json

from django.views    import View
from django.http     import JsonResponse

from products.models import Category, ProductDetailImage, SubCategory, Product, Tag

class ProductDetailView(View):
    def get(self, request, product_id):
        if not Product.objects.filter(id=product_id).exists():
            return JsonResponse({"MESSAGE":"INVALID_ID"}, status=404)

        categories    = Category.objects.all()
        subcategories = SubCategory.objects.all()
        product       = Product.objects.get(id=product_id)
        detail_page = {
            'categories'   : [category.name for category in categories],
            'subcategories': [subcategory.name for subcategory in subcategories],
            'id'           : product.id,
            'name'         : product.name,
            'thumbnail'    : product.thumbnail_image_url,
            'options'      : [{
                'size'  : option.size,
                'price' : option.price
                                } for option in product.option_set.all()],
            'tags'         : [tag.name for tag in product.tags.all()],
            'detail_img'   : ProductDetailImage.objects.get(product=product).image_url
        }
        return JsonResponse({"detail_page":detail_page}, status=200)

