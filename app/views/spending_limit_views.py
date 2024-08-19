import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_POST

from app.models import ShoppingList


@csrf_protect
@require_POST
def set_spending_limit(request):
    user = request.user
    data = json.loads(request.body)
    budget = data.get('budget')
    if budget:
        # Attempt to retrieve the latest ShoppingList for the user
        shopping_list = ShoppingList.objects.filter(user=user).order_by('-created_at').first()

        # Create a new ShoppingList if none exists
        if not shopping_list:
            shopping_list = ShoppingList.objects.create(user=user, spending_limit=budget)

        shopping_list.spending_limit = budget
        shopping_list.save()
        return JsonResponse({'success': True, 'budget': budget})
    return JsonResponse({'success': False}, status=400)