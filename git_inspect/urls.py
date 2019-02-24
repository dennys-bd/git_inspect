from django.conf import settings # noqa
from django.urls import path, re_path
from django.conf.urls import include
from django.contrib import admin
from django.views.generic import TemplateView
from rest_framework import routers
# from users.viewsets import UserViewSet, GroupViewSet
from users import views

import django_js_reverse.views

# router = routers.DefaultRouter()
# router.register(r'groups', GroupViewSet, base_name="Group")
# router.register(r'users', UserViewSet, base_name="User")

urlpatterns = [
    re_path(r'^admin/', admin.site.urls),
    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    path('register/', views.register),
    path('token/', views.token),
    path('token/refresh/', views.refresh_token),
    path('token/revoke/', views.revoke_token),
    # path('authentication/', include('users.urls')),

    re_path(r'^jsreverse/$', django_js_reverse.views.urls_js, name='js_reverse'),

    # re_path(r'^$', TemplateView.as_view(template_name='exampleapp/itworks.html'), name='home'),
    re_path(r'^$', TemplateView.as_view(template_name='loginapp/login.html'), name='home'),
    # path('', include(router.urls)),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        re_path(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
