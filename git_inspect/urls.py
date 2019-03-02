from django.conf import settings # noqa
from django.urls import path, re_path
from django.conf.urls import include
from django.contrib import admin
from django.views.generic import TemplateView
from rest_framework import routers

from repository.viewsets import RepositoryViewSet
from users import views
from loginapp import views as loginViews

import django_js_reverse.views

router = routers.DefaultRouter()
router.register(r'repositories', RepositoryViewSet, base_name='Repository')


urlpatterns = [
    re_path(r'^admin/', admin.site.urls),
    re_path(r'^$', TemplateView.as_view(template_name='loginapp/login.html'), name='home'),
    path('callback/', loginViews.callback),

    re_path(r'^jsreverse/$', django_js_reverse.views.urls_js, name='js_reverse'),

    path('', include(router.urls)),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        re_path(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
