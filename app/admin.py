from django.contrib import admin
from . import models
# Registering models for admin side
admin.site.register(models.ShoppingList)
admin.site.register(models.Item)
admin.site.register(models.Product)
