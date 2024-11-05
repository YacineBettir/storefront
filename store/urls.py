from django.urls import path,include
from . import views
from rest_framework_nested import routers
router=routers.DefaultRouter()

router.register('products',views.ProductViewSet,basename='products')
router.register('collections',views.CollectionViewSet,)
router.register('carts',views.CartViewSet,)
router.register('customers',views.CustomerViewSet)

product_router=routers.NestedDefaultRouter(router,'products',lookup='product')
product_router.register('reviews',views.ReviewViewSet,basename='product-reviews')

cart_router=routers.NestedDefaultRouter(router,'carts',lookup='cart')
cart_router.register('items',views.CartItemViewSet,basename='cart-items')




urlpatterns =[
    path('',include(router.urls)),
    path('',include(product_router.urls)),
    path('',include(cart_router.urls)),
    
    
]
