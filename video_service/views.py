from django.shortcuts import render

def home(request):
    # context = {
    #     'product_list': models.Product.objects.filter(is_active=True)[:settings.SHOP_LAST_INCOMING],
    #     }
    return render(request, 'video_service/home.html')