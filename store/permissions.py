from math import perm
from rest_framework import permissions

from core import serializers


class IsAdminOrReadOnly(permissions.BasePermission):
    
    def has_permission(self, request):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_staff)
    
class FullDjangoModelPermissions(permissions.DjangoModelPermissions):
    def __init__(self) -> None:
        self.perms_map['GET']=['%(app_label)s.view_%(model_name)s']
        


class ViewCustomerHistoryPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('store.view_history')
    

