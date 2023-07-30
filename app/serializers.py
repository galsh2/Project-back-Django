from rest_framework import serializers
from .models import  Cart, CartProduct, Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

# # class CartItemSerializer(serializers.ModelSerializer):
# #     class Meta:
# #         model = CartItem
# #         fields = ['id', 'product', 'quantity']

# class CartItemSerializer(serializers.ModelSerializer):
#     product = ProductSerializer(read_only=True)
#     product_id = serializers.IntegerField(write_only=True)

#     class Meta:
#         model = CartItem
#         fields = ('id', 'product', 'product_id', 'quantity')

#     def create(self, validated_data):
#         validated_data['cart'] = self.context['cart']
#         return super().create(validated_data)


# class CartProductSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = CartProduct
#         fields = ['product', 'quantity']

# class CartSerializer(serializers.ModelSerializer):
#     products = CartProductSerializer(source='cartproduct_set', many=True)

#     class Meta:
#         model = Cart
#         fields = ['user', 'products']

class CartProductSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = CartProduct
        fields = '__all__'
        # fields = ['product', 'quantity']

class CartSerializer(serializers.ModelSerializer):
    products = CartProductSerializer(source='cartitem_set', many=True)

    class Meta:
        model = Cart
        fields = '__all__'
        # fields = ['id', 'products']

