import json

from django.views    import View
from django.http     import JsonResponse

from banners.models  import Banner

class BannersView(View):
    def get(self, request):
        banners = Banner.objects.all()
        data = [{
            "product"  : banner.product.id,
            "image_url": banner.image_url
            } for banner in banners]

        return JsonResponse({'banners':data}, status=200)

