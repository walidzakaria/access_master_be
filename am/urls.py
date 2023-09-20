"""am URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.contrib.staticfiles.storage import staticfiles_storage
from django.urls import path, include, re_path

from authapp.views import PasswordReset
from .views import index, show_requests, with_id, with_title, register
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic import RedirectView
from rest_framework_swagger.views import get_swagger_view

admin.site.site_header = 'Red Sea 24'
admin.site.site_title = 'Red Sea 24'
schema_view = get_swagger_view(title='AM API')


urlpatterns = [
    re_path(r'^documentation/$', schema_view),
    path('admin/', admin.site.urls),
    path('explorer/', include('explorer.urls')),
    path('checkserver/', index, name='index'),
    path('api/auth/', include('authapp.urls')),
    path('api/entry/', include('entry.urls')),

    
    # For front-end pages
    path('', index, name='index'),
    
    path('login/', index, name='login'),
    path('forgot-password/', index, name='forgot-password'),
    path('auth/activate/<str:uid>/<str:token>/', register),
    path('auth/password/reset/confirm/<str:uid>/<str:token>/', register),
    path('app/change-password/', index, name='change-password'),

    # For favicons
    path('favicon.ico', RedirectView.as_view(url=staticfiles_storage.url('img/favicon.ico'))),
    path('favicon-32x32.png', RedirectView.as_view(url=staticfiles_storage.url('img/favicon-32x32.png'))),
    path('favicon-16x16.png', RedirectView.as_view(url=staticfiles_storage.url('img/favicon-16x16.png'))),
    path('apple-icon57x57.png',
         RedirectView.as_view(url=staticfiles_storage.url('img/apple-icon57x57.png'))),

    path('apple-touch-icon-180x180.png',
         RedirectView.as_view(url=staticfiles_storage.url('img/apple-touch-icon-180x180.png'))),
    path('apple-touch-icon-144x144.png',
         RedirectView.as_view(url=staticfiles_storage.url('img/apple-touch-icon-144x144.png'))),
    path('apple-touch-icon-114x114.png',
         RedirectView.as_view(url=staticfiles_storage.url('img/apple-touch-icon-114x114.png'))),
    path('apple-touch-icon-72x72.png',
         RedirectView.as_view(url=staticfiles_storage.url('img/apple-touch-icon-72x72.png'))),
    path('apple-touch-icon-57x57.png',
         RedirectView.as_view(url=staticfiles_storage.url('img/apple-touch-icon-57x57.png'))),
    path('social.jpg',
         RedirectView.as_view(url=staticfiles_storage.url('img/social.jpg'))),
]

# to enable viewing images in media directory
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
