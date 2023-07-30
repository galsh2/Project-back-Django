from django.db import IntegrityError
from django.http import Http404
from django.shortcuts import get_object_or_404, render

# Create your views here.

from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

# from app.models import Cart, CartItem, Product
# from app.serializers import CartItemSerializer, CartSerializer, ProductSerializer
# from app.serializers import CartItemSerializer, ProductSerializer
# from app.models import Cart, CartItem, Product
from app.models import Product
from app.serializers import ProductSerializer

############################################################# register #########################################################
# {   "username" : " ", "password" : " ", "email" : " "}

from django.contrib.auth.models import User
from rest_framework import status


class RegistrationAPIView(APIView):
    def post(self, request):
        # Extract the required data from the request
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')

        # Perform validation on the input data
        if not username or not email or not password:
            return Response({'error': 'Please provide all the required fields.'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the email is already taken
        if User.objects.filter(email=email).exists():
            return Response({'error': 'Email already exists.'}, status=status.HTTP_400_BAD_REQUEST)

        # Create a new user
        # try:
        #     user = User.objects.create_user(username=username, email=email, password=password)
        #     # Create a new cart for the user
        #     cart = Cart.objects.create(user=user)
        # except IntegrityError:
        #     return Response({'error': 'Username already exists.'}, status=status.HTTP_400_BAD_REQUEST)

        # Return a success responset
        return Response({'message': 'User registered successfully.'}, status=status.HTTP_201_CREATED)

################################################################### login ################################################################



# class ObtainTokenPairView(TokenObtainPairView):
#     def post(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)

#         user = serializer.validated_data['user']
#         token = serializer.validated_data

#         return Response({
#             'user': user.username,
#             'access_token': token['access'],
#             'refresh_token': token['refresh']
#         })

class ObtainTokenPairWithUsernameView(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.user  # use serializer.user instead
        # print(serializer.validated_data['access'])

        return Response({
            'username': user.username,
            'id': user.id,
            'access': str(serializer.validated_data['access']),
            'refresh': str(serializer.validated_data['refresh']),
        })

class LogoutAndBlacklistRefreshTokenForUserView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(status=200)
        except Exception as e:
            return Response(status=400)

############################################################# product #############################################################

class ProductAPIView(APIView):
    # permission_classes = (IsAuthenticated,)
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    

############################################################# cart #############################################################

# class prodtestview(TokenObtainPairView):
#     serializer_class = TokenObtainPairSerializer
#     token = serializer.validated_data['access']
#     def get(self, request):

#         if not to




from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Cart, Product
from .serializers import CartSerializer

class CartAPI(APIView):
    """
    Cart API for handling CRUD
    """

    def get(self, request):
        """
        Get a user's cart
        """
        user = request.user
        cart = Cart.objects.filter(user=user)
        serializer = CartSerializer(cart, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """
        Create a new cart or add product to existing cart
        """
        user = request.user
        product_id = request.data.get('product_id')

        # Assuming Cart and Product relationship as ManyToMany
        product = Product.objects.get(id=product_id)
        cart, created = Cart.objects.get_or_create(user=user, defaults={'products': [product]})

        if not created:
            # add product to existing cart
            cart.products.add(product)
        
        serializer = CartSerializer(cart)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def put(self, request):
        """
        Update a cart, like changing quantity of a product
        """
        user = request.user
        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity')

        cart = Cart.objects.get(user=user)
        cart_item = cart.cartitem_set.get(product_id=product_id)  # assuming you have CartItem model
        cart_item.quantity = quantity
        cart_item.save()

        serializer = CartSerializer(cart)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request):
        """
        Delete a product from cart
        """
        user = request.user
        product_id = request.data.get('product_id')

        cart = Cart.objects.get(user=user)
        product = Product.objects.get(id=product_id)
        cart.products.remove(product)

        serializer = CartSerializer(cart)
        return Response(serializer.data, status=status.HTTP_200_OK)

#############################################################################################################################

# # views.py
# from django.http import HttpResponse

# def display_cart(request):
#     cart_data = request.POST.get('cart_data')
#     print(cart_data)
#     return HttpResponse("Cart data received and printed in the terminal.")

import json
from rest_framework.views import APIView
from rest_framework.response import Response


class CartViewdis(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        cart_data = json.loads(request.data.get('cart'))
        # cart_data = request.data.get('cart')
        print(cart_data)
        # Perform other operations with the cart data
        return Response({'message': 'Cart data received'})
    
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

class PrintLoggedInUser(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        print(f"Logged-in User: {user}")
        return Response({"message": "User information printed on the Django terminal."})
    

from django.contrib.auth import authenticate, login
from django.http import JsonResponse

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            print(f"Username: {user.username}, User ID: {user.id}")  # Print the username and user id
            return JsonResponse({'message': 'Login successful'})
        else:
            return JsonResponse({'message': 'Invalid credentials'}, status=400)

    return JsonResponse({'message': 'Method not allowed'}, status=405)


# # class CartView(APIView):
# #     permission_classes = (IsAuthenticated,)

# #     def get(self, request):
# #         cart, _ = Cart.objects.get_or_create(user=request.user)
# #         serializer = CartItemSerializer(cart.items.all(), many=True)
# #         return Response(serializer.data)

# #     def post(self, request):
# #         cart, _ = Cart.objects.get_or_create(user=request.user)
# #         serializer = CartItemSerializer(data=request.data)
# #         if serializer.is_valid():
# #             serializer.save(cart=cart)
# #             return Response(serializer.data, status=201)
# #         return Response(serializer.errors, status=400)
        
# # class CartItemView(APIView):
# #     permission_classes = (IsAuthenticated,)

# #     def put(self, request, pk):
# #         # item = get_object_or_404(CartItem, pk=pk)
# #         cart_item = self.get_object(pk)
# #         serializer = CartItemSerializer(cart_item, data=request.data)
# #         if serializer.is_valid():
# #             serializer.save()
# #             return Response(serializer.data)
# #         return Response(serializer.errors, status=400)

# #     def delete(self, request, pk):
# #         item = get_object_or_404(CartItem, pk=pk)
# #         item.delete()
# #         return Response(status=204)

# from .models import Cart, CartProduct, Product
# from .serializers import CartSerializer, CartProductSerializer


# class CartAPI(APIView):
#     """
#     Retrieve, update or delete a cart instance.
#     """
#     def get_object(self, pk):
#         try:
#             return Cart.objects.get(pk=pk)
#         except Cart.DoesNotExist:
#             raise Http404

#     def get(self, request, format=None):
#         cart = get_object_or_404(Cart, user=request.user)
#         serializer = CartSerializer(cart)
#         return Response(serializer.data)

#     # # # def post(self, request, format=None):
#     # # #     user = request.user
#     # # #     product_id = request.data['product_id']
#     # # #     quantity = request.data['quantity']

#     # # def post(self, request, *args, **kwargs):
#     # #     user_id = request.data['user']
#     # #     for product in request.data['products']:
#     # #         product_id = product['product']
#     # #         quantity = product['quantity']

#     # #     cart, created = Cart.objects.get_or_create(user=user)
#     # #     product = get_object_or_404(Product, id=product_id)

#     # #     cart_product, created = CartProduct.objects.get_or_create(
#     # #         cart=cart, product=product, defaults={'quantity': quantity})

#     # #     if not created:
#     # #         cart_product.quantity += quantity
#     # #         cart_product.save()

#     # #     serializer = CartSerializer(cart)
#     # #     return Response(serializer.data, status=status.HTTP_201_CREATED)

#     # # def post(self, request, *args, **kwargs):
#     # #     user_id = request.data['user']
#     # #     user = User.objects.get(id=user_id)

#     # def post(self, request, *args, **kwargs):
#     #     user_identifier = request.data['user']
        
#     #     # Check if the user identifier is an ID or a username
#     #     if user_identifier.isdigit():
#     #         user = User.objects.get(id=user_identifier)
#     #     else:
#     #         user = User.objects.get(username=user_identifier)

#     #     for product in request.data['products']:
#     #         product_id = product['product']
#     #         quantity = product['quantity']

#     #         cart, created = Cart.objects.get_or_create(user=user)
#     #         product = get_object_or_404(Product, id=product_id)

#     #         cart_product, created = CartProduct.objects.get_or_create(
#     #             cart=cart, product=product, defaults={'quantity': quantity})

#     #         if not created:
#     #             cart_product.quantity += quantity
#     #             cart_product.save()

#     #     serializer = CartSerializer(cart)
#     #     return Response(serializer.data, status=status.HTTP_201_CREATED)

#     def post(self, request, *args, **kwargs):
#         user_identifier = request.data['user']
        
#         # Check if the user identifier is an ID or a username
#         if user_identifier.isdigit():
#             user = User.objects.get(id=user_identifier)
#         else:
#             user = User.objects.get(username=user_identifier)

#         for product in request.data['products']:
#             product_id = product['product']
#             quantity = product['quantity']

#             cart, created = Cart.objects.get_or_create(user=user)
#             product = get_object_or_404(Product, id=product_id)

#             cart_product, created = CartProduct.objects.get_or_create(
#                 cart=cart, product=product)

#             if not created:
#                 cart_product.quantity += quantity
#                 cart_product.save()
#             else:
#                 cart_product.quantity = quantity
#                 cart_product.save()

#         serializer = CartSerializer(cart)
#         return Response(serializer.data, status=status.HTTP_201_CREATED)

#     def put(self, request, format=None):
#         cart = get_object_or_404(Cart, user=request.user)
#         serializer = CartSerializer(cart, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def delete(self, request, format=None):
#         user = request.user
#         product_id = request.data['product_id']

#         cart = get_object_or_404(Cart, user=user)
#         product = get_object_or_404(Product, id=product_id)

#         cart_product = get_object_or_404(CartProduct, cart=cart, product=product)
#         cart_product.delete()

#         serializer = CartSerializer(cart)
#         return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
