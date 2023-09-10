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
import random
import string

from .models import QrCode, Entry
from .serializers import QrCodeSerializer, EntrySerializer


# Create your views here.
@api_view(['GET', ])
# @permission_classes([IsAuthenticated, ])
def create_qrs(request):
    """create 500 codes"""
    if request.method == 'GET':
        new_codes = [{'qr_code': generate_code()} for x in range(500)]
        serializer = QrCodeSerializer(data=new_codes, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(data={'result': 'OK'})
        return Response(data=serializer.errors, status=status.HTTP_200_OK)



@api_view(['POST', ])
# @permission_classes([IsAuthenticated, ])
def post_entry(request):
    """Post new entry"""
    if request.method == 'POST':
        qr = request.data.get('qr_code', '')
        # used_qr = Entry.objects.filter(qr_code__qr_code=qr).first()
        # if used_qr:
        #     return Response(data={'result': 'this QR code is already used.'}, status=status.HTTP_200_OK)
        qr_code = QrCode.objects.filter(qr_code=qr).first()
        if not qr_code:
            return Response(data={'result': 'This qr doesn''t exist'}, status=status.HTTP_200_OK)
        
        used_qr_code = Entry.objects.filter(qr_code=qr_code.id).first()
        if used_qr_code:
            return Response(data={'result': 'This qr already used.'}, status=status.HTTP_200_OK)

        request.data['qr_code'] = qr_code.id
        serializer = EntrySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(data=serializer.errors, status=status.HTTP_200_OK)
        

def generate_code():
    characters = string.ascii_letters + string.digits # include letters and digits
    random_string = ''.join(random.choice(characters) for _ in range(14))
    return random_string