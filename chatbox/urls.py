from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import ChatboxViewSet


router=DefaultRouter()
router.register('messages',ChatboxViewSet,basename='chatmesaage')


urlpatterns=[
    path('',include(router.urls)),
    
]