import json

from django.views               import View
from django.http                import JsonResponse
from django.db.models           import Sum, F
from django.db.models.functions import Coalesce

from carts.models    import Cart
from products.models import Option, Product
from users.utils     import login_required

class CartsView(View):
    @login_required
    def post(self, request):
        try:
            data         = json.loads(request.body)
            user         = request.user
            request_list = data['request_list']

            for request in request_list:
                product_id = request['product_id']
                option_id  = request['option_id']
                quantity   = int(request['quantity'])

                if not Product.objects.filter(id=product_id).exists():
                    return JsonResponse({"message":"INVALID_PRODUCT_ID"}, status=404)

                if not Option.objects.filter(id=option_id).exists():
                    return JsonResponse({"message":"INVALID_PRODUCT_ID"}, status=404)

                option = Option.objects.get(id=option_id)

                if option.product_id != int(product_id):
                    return JsonResponse({"message":"INVALID_OPTION"}, status=404)

                cart, created = Cart.objects.get_or_create(
                    user       = user,
                    product_id = product_id,
                    option_id  = option_id,
                    defaults   = {
                        'quantity' : 0
                    })
                cart.quantity += quantity
                cart.save()      
            return JsonResponse({"message":"SUCCESS"}, status=201)
        except KeyError:
            return JsonResponse({"message":"KEY_ERROR"}, status=400)
    
    @login_required
    def get(self, request):
        user = request.user

        cart_list = [{
            'id'           : item.id,
            'product_name' : item.product.name,
            'quantity'     : item.quantity,
            'size'         : item.option.size,
            'product_price': item.option.price,
            'image_url'    : item.product.thumbnail_image_url,
            'price'        : int(item.option.price) * int(item.quantity)
        } for item in Cart.objects.filter(user=user)]

        total_price = Cart.objects.filter(user=user).aggregate(total=Sum(F('option__price')*F('quantity')))['total'] or 0
        free_shipping  = 20000
        shipping_price = 0 if total_price > free_shipping or not total_price else 2500   

        return JsonResponse({
            "Cart"       : cart_list,
            "shipping"   : shipping_price,
            "total_price": total_price
            }, status=200)

