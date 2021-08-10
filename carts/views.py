import json

from django.views import View
from django.http  import JsonResponse

from carts.models    import Cart
from products.models import Option
from users.utils     import login_required

class CartsView(View):
    @login_required
    def post(self, request):
        try:
            data       = json.loads(request.body)
            user       = request.user
            product_id = data['product_id']
            option_id  = data['option_id']
            quantity   = int(data['quantity'])

            option = Option.objects.get(id=option_id)
            if option.product_id != product_id:
                return JsonResponse({"message":"INVALID_OPTION"}, status=404)

            if Cart.objects.filter(user=user, option_id=option_id, product_id=product_id).exists():
                item = Cart.objects.get(
                    user       = user,
                    product_id = product_id,
                    option_id  = option_id)
                item.quantity += quantity
                item.save()
                return JsonResponse({"message":"SUCCESS"}, status=200)

            Cart.objects.create(
                user       = user,
                product_id = product_id,
                quantity   = quantity,
                option_id  = option_id)
            return JsonResponse({"message":"SUCCESS"}, status=201)
        except KeyError:
            return JsonResponse({"message":"KEY_ERROR"}, status=400)
    
    @login_required
    def get(self, request):
        user = request.user
        cart_list = [{
            'id'          : item.id,
            'product_name': item.product.name,
            'quantity'    : item.quantity,
            'size'        : item.option.size,
            'price'       : item.option.price,
            'image_url'   : item.product.thumbnail_image_url
        } for item in Cart.objects.filter(user=user)]
        return JsonResponse({"CART_LIST": cart_list}, status=200)

