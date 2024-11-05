from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter,OrderingFilter
from rest_framework.response import Response
from rest_framework.mixins import CreateModelMixin,RetrieveModelMixin,DestroyModelMixin
from rest_framework import status
from rest_framework.viewsets import GenericViewSet,ModelViewSet
from .models import Product,OrderItem,Collection,Review,Cart,CartItem
from .serializers import UpdateCartItemSerializer,ProductSerializer,CollectionSerializer,AddCartItemSerializer,ReviewSerializer,CartSerializer,CartItemSerializer
from .filters import ProductFilter
from .pagination import DefaultPagination

class ProductViewSet(ModelViewSet):
    queryset=Product.objects.all()
    serializer_class=ProductSerializer    
    filter_backends=[DjangoFilterBackend,SearchFilter,OrderingFilter]
    filterset_class=ProductFilter
    search_fields=['title','description']    
    ordering_fields=['unit_price','last_update']
    pagination_class=DefaultPagination
    
    
    def get_serializer_context(self):
        return {'request':self.request}  

    def destroy(self,*args, **kwargs):
        if OrderItem.objects.filter(product_id=kwargs['pk']).exists():
             return Response(
                {
                "error":'THIS ITEM HAS AN ACTIVE ORDERITEM RESOLVE BEFORE DELETING'
                },status=status.HTTP_409_CONFLICT)
        return super().destroy(self.request,*args, **kwargs)
        

class CollectionViewSet(ModelViewSet):
    queryset=Collection.objects.annotate(
        products_count=Count('products')).all()  
    serializer_class=CollectionSerializer
    
    def destroy(self,*args, **kwargs):
        if Product.objects.filter(collection_id=kwargs['pk']).exists():
            return Response(
                {"error":'THIS COLLECTION HAS A PRODUCT ASSOICIATED WITH IT'
                 },status=status.HTTP_409_CONFLICT)
        return super().destroy(self.request,*args, **kwargs)
    
class ReviewViewSet(ModelViewSet):
    serializer_class=ReviewSerializer
    
    def get_queryset(self):
        return Review.objects.filter(product_id=self.kwargs['product_pk'])
    
    def get_serializer_context(self):
        return {'product_id':self.kwargs['product_pk']}
    
    
class CartViewSet(CreateModelMixin, 
                  RetrieveModelMixin,
                  DestroyModelMixin, 
                  GenericViewSet):
    queryset=Cart.objects.prefetch_related('items__product').all()
    serializer_class=CartSerializer
    
    
    
class CartItemViewSet(ModelViewSet):
    http_method_names=['post','get','patch','delete']
    
    def get_serializer_class(self):
        if self.request.method == "POST":
            return AddCartItemSerializer
    
        elif self.request.method == 'PATCH':
            return UpdateCartItemSerializer
        else:
            return CartItemSerializer
    
    
    def get_serializer_context(self):
        return {'cart_id':self.kwargs['cart_pk']}
    
    def get_queryset(self):
        return CartItem.objects \
            .filter(cart_id=self.kwargs['cart_pk'])\
            .select_related('product')
        