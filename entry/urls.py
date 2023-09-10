from django.urls import path, include, re_path
from .views import create_qrs, post_entry

urlpatterns = [
    path('create/', create_qrs, name='create-qrs'),
    path('enter/', post_entry, name='post-entry'),
]