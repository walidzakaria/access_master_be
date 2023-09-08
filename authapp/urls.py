from django.urls import path, include, re_path
from .views import PasswordReset, check_token, restricted, get_user_info, CustomTokenCreateView

urlpatterns = [
    path('token/login/', CustomTokenCreateView.as_view(), name='token-login'),
    path('', include('djoser.urls')),
    path('', include('djoser.urls.authtoken')),
    path('', include('djoser.urls.jwt')),
    path('restricted/', restricted),
    path('password/reset/confirm/<str:uid>/<str:token>/', PasswordReset.as_view()),
    path('check-token/', check_token, name='check-token'),
    path('get-info/', get_user_info, name='get-info'),
]