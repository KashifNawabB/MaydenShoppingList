from django.urls import path
from django.contrib.auth.decorators import login_required
from .views.home_views import *
from .views.cart_views import *
from .views.spending_limit_views import *


urlpatterns = [
    path('', login_required(index), name='index'),
    path('items/', login_required(my_cart_view), name='cart'),
    path('add-to-cart/', login_required(add_to_cart), name='add_to_cart'),
    path('remove-from-cart/', login_required(remove_from_cart), name='remove-from-cart'),
    path('mark-as-bought/', login_required(mark_as_bought), name='mark-as-bought'),
    path('update-quantity/', login_required(update_quantity), name='update-quantity'),
    path('update-cart-order/', login_required(update_cart_order), name='update-cart-order'),
    path('share-cart/', login_required(share_cart), name='share_cart'),
    path('set-spending-limit/', login_required(set_spending_limit), name='set-spending-limit'),
]