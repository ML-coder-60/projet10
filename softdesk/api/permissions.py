from rest_framework import permissions
from api.models import Contributors
from django.db.models import Q


class IsCurrentUserOwnerOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        print(request.method)
        print(view.kwargs)
        if request.user and request.user.is_authenticated:
            if request.method in permissions.SAFE_METHODS:
                print(request.method)
                return True
            else:
                if Contributors.objects.filter(
                            Q(project_id=view.kwargs['id_project']) &
                            Q(user_id=request.user.id) &
                            Q(permission='Créateur')).exists():
                    return True
        return False
