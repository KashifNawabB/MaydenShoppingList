from app.models import Item, ShoppingList


def update_expense(user):
    cart = Item.objects.filter(shopping_list__user=user).order_by('order')
    shopping_list = ShoppingList.objects.filter(user=user).order_by('-created_at').first()

    # Calculate total price
    total_price = sum(item.total_cost for item in cart)
    # Calculate if the total price exceeds the spending limit
    spending_limit = shopping_list.spending_limit or 0
    exceeds_limit = total_price > spending_limit
    exceed_amount = total_price - spending_limit if exceeds_limit else 0
    data = {
        'cart': cart,
        'shopping_list': shopping_list,
        'total_price': total_price,
        'exceeds_limit': exceeds_limit,
        'exceed_amount': exceed_amount,
    }
    return data


