"""
    softdesk URL Configuration
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework import routers

from authentication.views import ChangePasswordView
from api.views import ProjectViewset, UserAPIView, IssuesViewset, \
                      CommentsViewset, ContributorsViewset, CustomTokenObtainPairView

router = routers.SimpleRouter()
router.register('', ProjectViewset, basename='projects')
router.register('(?P<id_project>[^/.]+)/users', ContributorsViewset, basename='users')
router.register('(?P<id_project>[^/.]+)/issues', IssuesViewset, basename='issues')
router.register('(?P<id_project>[^/.]+)/issues/(?P<id_issue>[^/.]+)/comments', CommentsViewset, basename='comments')

urlpatterns = [
#    demo/debug
#    path('admin/', admin.site.urls),
#    path('api-auth/', include('rest_framework.urls')),
#    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
#    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('', RedirectView.as_view(url='login/')),
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('signup/', UserAPIView.as_view()),
    path('projects/', include(router.urls), name='projects'),
]
