from rest_framework import permissions

class IsOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.borrower == request.user
    
class IsInvestor(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.user_type == 'I'

class IsBorrower(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.user_type == 'B'