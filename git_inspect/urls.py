from django.conf import settings # noqa
# from django.urls import path, re_path
from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import TemplateView
from rest_framework import routers
from users.viewsets import UserViewSet, GroupViewSet

import django_js_reverse.views

router = routers.DefaultRouter()
router.register(r'groups', GroupViewSet, base_name="Group")
router.register(r'users', UserViewSet, base_name="User")

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),

    url(r'^jsreverse/$', django_js_reverse.views.urls_js, name='js_reverse'),

    url(r'^$', TemplateView.as_view(template_name='exampleapp/itworks.html'), name='home'),
    url('', include(router.urls)),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
