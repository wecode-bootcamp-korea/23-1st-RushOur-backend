import json
from my_settings import SECRET_KEY

from wishlists.models import Wishlist

from django.http            import JsonResponse
from django.views           import View
from django.db.models       import Q
from products.models        import (Category,SubCategory,Product,Option,ProductDetailImage,Tag,)
from users.utils             import login_required 
from users.models            import User


class WishlistView(View):
    @login_required
    def get(self, request):
        try:
            user=User.objects.get(id=request.user.id)
            like_list      = user.wishlist_set.all()
            
            like_items = [{
            'product_id'  : product.id,
            'name'        : product.name, 

        }for product in like_list]
        except KeyError:
            return JsonResponse({'Message' : 'KEY_ERROR'}, status = 400)
        return JsonResponse({'Like_Items' : like_items}, status = 200)
    
    @login_required
    def post(self,request):
        try:
            data           = json.loads(request.body)
            product_id     = data.get('product_id')
            user_id        = request.user.id
 
            if Wishlist.objects.filter(Q(product_id=product_id) & Q(user_id=user_id)).exists():
               Wishlist.objects.filter(product_id=product_id).delete()
               return JsonResponse({'Message' : 'SUCCESS_DELETE'}, status = 200)
        

            else:
                Wishlist.objects.create(
                product_id    = data['product_id'],
                user_id       = user_id

                ) 

        except KeyError:
            return JsonResponse({'Message' : 'KEY_ERROR'}, status = 400)

        return JsonResponse({'Message' : 'SUCCESS_CREATE'}, status = 200)