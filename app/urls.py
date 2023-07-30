
# from django.contrib import admin
from django.urls import path
from app import views

# from app.views import CartAPIView, CartItemAPIView, LogoutAndBlacklistRefreshTokenForUserView, ObtainTokenPairWithUsernameView, ProductAPIView, RegistrationAPIView
from app.views import CartAPI, CartViewdis, LogoutAndBlacklistRefreshTokenForUserView, ObtainTokenPairWithUsernameView, PrintLoggedInUser, ProductAPIView, RegistrationAPIView
urlpatterns = [
    # path('admin/', admin.site.urls),
    path('app/product/', ProductAPIView.as_view(), name='Product'),
    path('app/register/', RegistrationAPIView.as_view(), name='Register'),
    path('app/token/', ObtainTokenPairWithUsernameView.as_view(), name='token_obtain_pair'),
    path('app/token/blacklist/', LogoutAndBlacklistRefreshTokenForUserView.as_view(), name='token_blacklist'),
#     # # path('app/cart/', CartAPIView.as_view(), name='cart'),
#     # # path('app/cart/<int:cart_id>/items/', CartItemAPIView.as_view(), name='cart-items'),
#     # # path('app/cart/<int:cart_id>/items/<int:item_id>/', CartItemAPIView.as_view(), name='cart-item'),
#     # path('app/cart/', CartAPIView.as_view(), name='cart-detail'),
#     # # path('cart/', CartAPIView.as_view(), name='cart'),
#     # path('app/cart-items/', CartItemAPIView.as_view(), name='cartitem-list'),
#     # # path('app/cart-items/<int:pk>/', CartItemAPIView.as_view(), name='cartitem-detail'),
#     # path('app/cart-items/<int:cart_item_id>/', CartItemAPIView.as_view(), name='cart-item'),
#     # path('app/cart-items/', CartItemListView.as_view(), name='cart-items'),
#     # path('app/cart-items/add/', CartItemAddView.as_view(), name='cart-item-add'),
#     # path('app/cart-items/remove/<int:pk>/', CartItemRemoveView.as_view(), name='cart-item-remove'),
#     # path('app/cart-items/update/<int:pk>/', CartItemUpdateView.as_view(), name='cart-item-update'),
#     path('app/cart/', CartView.as_view(), name='cart'),
#     path('app/cart-item/<int:pk>/', CartItemView.as_view(), name='cart-item'),
#     # path('app/cart-item/', CartItemView.as_view(), name='update_cart_item'),
    path('app/cart/', CartAPI.as_view(), name='cart'),
    # path('app/dis/', display_cart, name='display_cart'),
    path('app/cartdis/', CartViewdis.as_view(), name='cart2'),
    # path('print_logged_in_user/', views.print_logged_in_user, name='print_logged_in_user'),
    path('print_logged_in_user/', views.user_login, name='print_logged_in_user'),
    path('app/user', PrintLoggedInUser.as_view(), name='print-logged-in-user'),
    
]
