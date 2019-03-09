from django.conf import settings  # noqa
from django.conf.urls import include
from django.contrib import admin
from django.urls import path, re_path
from django.views.generic import TemplateView

import django_js_reverse.views
from rest_framework import routers

from repositories.viewsets import CommitViewSet, RepositoryViewSet
from users import views as user_views


router = routers.DefaultRouter()
router.register(r'repositories', RepositoryViewSet, base_name='Repository')
router.register(r'commits', CommitViewSet, base_name='Commit')


urlpatterns = [
    re_path(r'^admin/', admin.site.urls),
    re_path(r'^$', TemplateView.as_view(template_name='rootapp/home.html'), name='home'),
    path('login', TemplateView.as_view(template_name='rootapp/home.html'), name='login'),
    path('callback/', user_views.callback),
    path('verifytoken', user_views.verify_token),
    path('checkcommits', user_views.check_for_commits),


    re_path(r'^jsreverse/$', django_js_reverse.views.urls_js, name='js_reverse'),
    path('', include(router.urls)),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        re_path(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
