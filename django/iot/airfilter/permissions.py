from rest_framework import permissions

class AdminWriteOrUserReadOnly(permissions.BasePermission):
    def has_permission(self,request,view):
        if request.user.is_authenticated:
            if request.user.is_staff :
                return True
            elif request.user.has_perm('airfilter.add_airkorea'):
                return True
            elif request.method in permissions.SAFE_METHODS :
                return True
            else :
                return False

        return False

    def has_object_permission(self,request,view,obj):
        if request.user.is_staff or (request.method in permissions.SAFE_METHODS):
            return True

        return False

