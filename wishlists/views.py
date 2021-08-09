import json
from wishlists.models import Wishlist

from django.http            import JsonResponse
from django.views           import View
from django.db.models       import Q

from products.models        import (Category,SubCategory,Product,Option,ProductDetailImage,Tag)
from util.utils             import login_required
        


class WishlistView(View):
    @login_required
    def get(self, request):
        like_list      = request.user.product_set.all()
        
        like_items = [{
            'product_id'  : product.id,
            'name'        : product.name, 
            'tag'         : product.tag,
            'price'       : product.productoption_set.first().price,
            'image_url'   : product.productimage_set.first().image_url,
        }for product in like_list]
        
        return JsonResponse({'Like_Items' : like_items}, status = 200)
    
    @login_required
    def post(self,request):
        try:
            data           = json.loads(request.body)
            product_id     = data.get('product_id')
            like_list      = request.user.product_set.all()

            if Wishlist.objects.filter(product_id=product_id, user=request.user).exists():
                request.user.product_set.remove(product_id)

            else:    
                request.user.product_set.add(product_id)

        except KeyError:
            return JsonResponse({'Message' : 'KEY_ERROR'}, status = 400)

        except Product.DoesNotExist:
            return JsonResponse({'Message' : 'NOT_FOUND_PRODUCT'}, status = 404)

        return JsonResponse({'Message' : 'SUCCESS'}, status = 200)
