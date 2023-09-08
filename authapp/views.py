# from django.contrib.sites import requests
import requests
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status, generics, views
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from djoser.conf import django_settings

from djoser.views import TokenCreateView
from rest_framework.throttling import UserRateThrottle
from axes.decorators import axes_dispatch
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt


from .models import User


# Create your views here.
from .serializers import CurrentUserSerializer, UserInfoSerializer


@api_view(['GET'])
def restricted(request, *args, **kwargs):
    return Response(data='Only for logged-in users', status=status.HTTP_200_OK)


# class ActivateUser(GenericAPIView):

#     def get(self, request, uid, token, format=None):
#         payload = {'uid': uid, 'token': token}
#         protocol = 'https://' if request.is_secure() else 'http://'
#         domain = request.get_host()
#         url = f"{protocol}{domain}/auth/users/activation/"
#         response = requests.post(url, data=payload)

#         if response.status_code == 204:
#             return Response({}, response.status_code)
#         else:
#             return Response(response.json())

@method_decorator(axes_dispatch, name='dispatch')
@method_decorator(csrf_exempt, name='dispatch')
class CustomTokenCreateView(TokenCreateView):
    def post(self, request, *args, **kwargs):
        print('test....')
        throttle_classes = [UserRateThrottle]
        return super().post(request, *args, **kwargs)


class PasswordReset(GenericAPIView):

    def get(self, request, uid, token, format=None):
        payload = {'uid': uid, 'token': token}

        return JsonResponse(payload)


@api_view(['GET', ])
@permission_classes([IsAuthenticated])
def check_token(request):
    if request.method == 'GET':
        return Response(data={'details': 'token is valid'}, status=status.HTTP_200_OK)


@api_view(['GET', ])
@permission_classes([IsAuthenticated, ])
def get_user_info(request):
    if request.method == 'GET':
        user = request.user
        serializer = UserInfoSerializer(user)
        print('logged user', user)
        return Response(serializer.data, status=status.HTTP_200_OK)