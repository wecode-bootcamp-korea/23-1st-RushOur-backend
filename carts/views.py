import json

from django.views import View
from django.http  import JsonResponse

from carts.models import Cart
from users.utils  import login_required

class CartView(View):
    @login_required
    def patch(self, request, cart_id):
        try:
            if not Cart.objects.filter(id = cart_id).exists():
                return JsonResponse({"message":"INVALID_CART_ID"}, status=404)
 
            data = json.loads(request.body)
            user = request.user
            item = Cart.objects.get(id = cart_id)

            if item.user != user:
                return JsonResponse({"message":"NOT_AUTH_USER"}, status=403)

            item.quantity = int(data['quantity'])
            item.save()
            return JsonResponse({
                "message"  : "SUCCESS", 
                "QUANTITY" : item.quantity}, status = 201)
        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status=400)

    @login_required
    def delete(self, request, cart_id):
        try:
            if not Cart.objects.filter(id = cart_id).exists():
                return JsonResponse({"message":"INVALID_CART_ID"}, status=404)

            user = request.user    
            item = Cart.objects.get(id = cart_id)
            
            if item.user != user:
                return JsonResponse({"message":"NOT_AUTH_USER"}, status=403)

            item.delete()
            return JsonResponse({"message":"SUCCESS_DELETE"}, status=200)
        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status=400)