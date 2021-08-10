import json

from django.views import View
from django.http  import JsonResponse

from carts.models import Cart
from users.utils  import login_required

class CartView(View):
    @login_required
    def patch(self, request, cart_id):
        try: 
            data = json.loads(request.body)
            item = Cart.objects.get(id = cart_id)
            item.quantity = int(data['quantity'])
            item.save()
            return JsonResponse({
                "message"  : "SUCCESS", 
                "QUANTITY" : item.quantity, 
                "PRICE"    : item.option.price * int(item.quantity)}, status=201)

        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status=400)