from rest_framework import permissions




#non user can't have acces to edit
class IsAdminOrReadOnly(permissions.IsAdminUser):
    #allow access to user admin

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        else:
            return bool(request.user and request.user.is_staff)





class IsReviewUserOrReadOnly(permissions.BasePermission):


    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            #check permission for read only request
            return True

        else:

            #check permission for write request
                   # Here getting who worte review == curent login user
            return obj.review_user == request.user or request.user.is_staff



