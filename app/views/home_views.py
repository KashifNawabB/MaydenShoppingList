from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from app.models import ShoppingList, Product


@csrf_protect
def index(request):
    user = request.user
    products = Product.objects.all()
    shopping_list = ShoppingList.objects.filter(user=user).order_by('-created_at').first()
    data = {
        'products': products,
        'shopping_list': shopping_list
    }
    return render(request, 'index.html', context=data)






