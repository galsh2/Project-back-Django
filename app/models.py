from django.db import models
from django.forms import ValidationError
from django.contrib.auth.models import User
# Create your models here.

class Brand(models.Model):  #new
    name = models.CharField(max_length=55)

    def __str__(self):
        return self.name

class Product(models.Model):
    PRODUCT_TYPES = (
        ('SH', 'Shoes'),
        ('SHI', 'Shirt'),
        ('PA', 'Pants'),
    )
    Category_TYPES = (   
        ('Men', 'Men'),
        ('Womens', 'Womens'),
        ('Unisex', 'Unisex'),
    )

    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    product_type = models.CharField(max_length=3, choices=PRODUCT_TYPES)
    category_type = models.CharField(max_length=6, choices=Category_TYPES)
    brand = models.ForeignKey('Brand', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class ProductVariant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    size = models.CharField(max_length=10)
    stock = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.product.name} - Size: {self.size}, Stock: {self.stock}"
    
    def save(self, *args, **kwargs): #new
        if ProductVariant.objects.filter(product=self.product, size=self.size).exists():
            raise ValidationError("Variant with this size already exists.")
        super().save(*args, **kwargs)

# class Cart(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)

# class CartItem(models.Model):
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
#     quantity = models.PositiveIntegerField(default=1)

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField('Product', through='CartProduct')

class CartProduct(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)



