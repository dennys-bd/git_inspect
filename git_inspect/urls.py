'''
project routers
'''
from django.conf import settings  # noqa
from django.conf.urls import include
from django.contrib import admin
from django.urls import path, re_path
from django.views.generic import TemplateView

import django_js_reverse.views


urlpatterns = [
    re_path(r'^admin/', admin.site.urls),
    re_path(r'^$', TemplateView.as_view(template_name='rootapp/home.html'), name='home'),
    path('login', TemplateView.as_view(template_name='rootapp/home.html'), name='login'),
    path('api/', include('repositories.urls')),
    path('api/', include('users.urls')),

    re_path(r'^jsreverse/$', django_js_reverse.views.urls_js, name='js_reverse'),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        re_path(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
