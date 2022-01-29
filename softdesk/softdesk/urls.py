"""softdesk URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework import routers

from rest_framework.decorators import action

from authentication.views import ChangePasswordView
from api.views import   ProjectViewset, \
                        UserAPIView, \
                        IssuesViewset, \
                        CommentsViewset, \
                        ContributorsViewset, \
                        CustomTokenObtainPairView

router = routers.SimpleRouter()
router.register('', ProjectViewset, basename='projects')
router.register('(?P<id_project>[^/.]+)/users', ContributorsViewset, basename='users')
router.register('(?P<id_project>[^/.]+)/issues', IssuesViewset, basename='issues')
router.register(
    '(?P<id_project>[^/.]+)/issues/(?P<id_issue>[^/.]+)/comments',
    CommentsViewset,
    basename='comments'
)

urlpatterns = [
    path('', RedirectView.as_view(url='projects/')),
    path('projects/', include(router.urls), name='projects'),
    path('signup/', UserAPIView.as_view()),
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('api-auth/', include('rest_framework.urls')),
    path('admin/', admin.site.urls)
]
