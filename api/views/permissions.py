from rest_framework.permissions import BasePermission
from api.choices import ROLE


class IsAdminOnly(BasePermission):
    '''
        Permission is for Admin only(AD)
    '''
    message = 'Not allowed.'
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return request.user.role == "AD"

class IsAdminOrManager(BasePermission):
    '''
        Permission is for Admin(AD) and Manager(MN)
    '''
    message = 'Not allowed.'
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return request.user.role in ['AD', 'MN']


class IsAll(BasePermission):
    message = 'Not allowed.'
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return request.user.role in ['AD', 'MN', 'EM']