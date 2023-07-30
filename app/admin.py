from django.contrib import admin

# Register your models here.

# from app.models import Brand, Cart, CartItem, Product, ProductVariant
from app.models import Brand, Cart, CartProduct, Product, ProductVariant
# Register your models here.

admin.site.register(Product)
admin.site.register(ProductVariant)
admin.site.register(Cart)
admin.site.register(CartProduct)
admin.site.register(Brand)