import json
from django.core.mail import send_mail
from django.db import models
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_POST

from app.models import Item, ShoppingList, Product
from app.services.expense_service import update_expense
from shopping_list import settings


@csrf_protect
def my_cart_view(request):
    user = request.user
    data = update_expense(user)
    return render(request, 'cart.html', context=data)

@csrf_protect
@require_POST
def add_to_cart(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        product_id = data.get('product_id')
        product = get_object_or_404(Product, id=product_id)
        user = request.user

        if product:
            # Retrieve or create the shopping list for the user
            shopping_list, created = ShoppingList.objects.get_or_create(user=user)
            # Check if the item already exists in the shopping list
            cart_item = Item.objects.filter(
                shopping_list=shopping_list,
                name=product.name
            ).first()

            if cart_item:
                # Item exists, increment the quantity
                cart_item.quantity += 1
                cart_item.save()
                return JsonResponse({'success': True, 'incremented': True})
            else:
                # Item does not exist, create a new one
                # Retrieve the maximum value of the 'order' field
                max_order = Item.objects.filter(shopping_list=shopping_list).aggregate(models.Max('order'))['order__max']

                # Determine the new order value
                new_order_value = (max_order or 0) + 1

                Item.objects.create(
                    shopping_list=shopping_list,
                    name=product.name,
                    price=product.price,
                    quantity=1,  # Set initial quantity to 1
                    order=new_order_value
                )

                return JsonResponse({'success': True})

    return JsonResponse({'success': False}, status=400)

@csrf_protect
def remove_from_cart(request):
    if request.method == 'POST':
        user = request.user
        data = json.loads(request.body)
        product_id = data.get('product_id')
        item = get_object_or_404(Item, id=product_id)

        # Delete the item from the cart
        item.delete()

        data = update_expense(user)

        return JsonResponse({
            'success': True,
            'total_price': data.get('total_price'),
            'exceeds_limit': data.get('exceeds_limit'),
            'exceed_amount': data.get('exceed_amount'),
        })

    return JsonResponse({'success': False}, status=400)

@csrf_protect
@require_POST
def mark_as_bought(request):
    try:
        data = json.loads(request.body)
        product_id = data.get('product_id')
        bought_status = data.get('bought')
        print(data)

        # Retrieve the item based on the product ID and the user's shopping list
        item = get_object_or_404(Item, id=product_id, shopping_list__user=request.user)

        # Update the 'bought' status of the item
        item.bought = bought_status
        item.save()

        return JsonResponse({'success': True})

    except Item.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Item not found.'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

@csrf_protect
@require_POST
def update_quantity(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        product_id = data.get('product_id')
        new_quantity = data.get('quantity')
        print(data)
        # Fetch the item and update quantity
        item = get_object_or_404(Item, id=product_id)
        if item:
            item.quantity = new_quantity
            item.save()
            data = update_expense(request.user)
            return JsonResponse({
                'success': True,
                'total_price': data.get('total_price'),
                'exceeds_limit': data.get('exceeds_limit'),
                'exceed_amount': data.get('exceed_amount'),
            })

    return JsonResponse({'success': False}, status=400)

@csrf_protect
@require_POST
def update_cart_order(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        order = data.get('order', [])

        for index, item_id in enumerate(order):
            try:
                item = Item.objects.get(id=item_id)
                item.order = index
                item.save()
            except Item.DoesNotExist:
                return JsonResponse({'success': False}, status=400)

        return JsonResponse({'success': True})

    return JsonResponse({'success': False}, status=400)


def share_cart(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        shopping_list_id = request.POST.get('shopping_list_id')
        shopping_list = get_object_or_404(ShoppingList, id=shopping_list_id)
        cart_items = shopping_list.items.all()
        if cart_items.count() < 1:
            return JsonResponse({'success': False, 'message': 'Cart is empty.'})

        cart_content = "\n".join([
                        f"{item.name} - {item.quantity} x £{item.price} {'(Bought)' if item.bought else ''}"
                        for item in cart_items
                    ])


        from_email = settings.DEFAULT_FROM_EMAIL
        subject = f"My Shopping List"
        message = f"""
Hi Dear,

I’ve put together a shopping list that I need your help with. When you have a moment, could you please pick these up?

Shopping List:
{cart_content}
    
Thank you so much for taking care of this!

Regards,
{request.user.username}
        """

        try:
            send_mail(subject, message, from_email, [email])
            return JsonResponse({'success': True, 'message': 'Cart shared successfully!'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})

    return JsonResponse({'success': False, 'message': 'Invalid request method.'})