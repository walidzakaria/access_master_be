# from django.contrib.sites import requests
from pytz import timezone
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


from .models import Branch, PrintOrder, QrCode, Entry
from .serializers import (
    BranchSerializer, QrCodeSerializer,
    EntrySerializer, BranchEntriesSerializer
)
from .utils import create_pdf, generate_code


# Create your views here.
@api_view(['GET', ])
# @permission_classes([IsAuthenticated, ])
def create_qrs(request):
    """create 500 codes"""
    if request.method == 'GET':
        user = request.user
        if user.get_type() != 'admin':
            return Response(data={'result': 'Invalid user!'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        
        new_print_order = PrintOrder()
        new_print_order.save()
        
        new_codes = [{
            'print_order': new_print_order.id,
            'qr_code': generate_code()
            } for x in range(500)]
        serializer = QrCodeSerializer(data=new_codes, many=True)
        if serializer.is_valid():
            serializer.save()
            base_url = request.build_absolute_uri('/')
            code_list = [ f"{base_url}entry/{i['qr_code']}" for i in new_codes]
            return create_pdf(code_list)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_branches(request):
    """List all branches"""
    if request.method == 'GET':
        branches = Branch.objects.all()
        
        serializer = BranchSerializer(branches, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_branches_entries(request):
    """List all branches with number of entries"""
    if request.method == 'GET':
        branches = Branch.objects.all()
        
        serializer = BranchEntriesSerializer(branches, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_daily_entries(request, branchId):
    """List daily entries"""
    if request.method == 'GET':
        entries = Entry.objects.filter(entry_time__date=timezone.now)
        
        if branchId != 0:
            entries = entries.filter(branch=branchId)
        
        serializer = EntrySerializer(entries, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated, ])
def post_entry(request):
    """Post new entry"""
    if request.method == 'POST':
        qr = request.data.get('qr_code', '')

        qr_code = QrCode.objects.filter(qr_code=qr).first()
        if not qr_code:
            return Response(data={'result': 'This QR code is invalid!'}, status=status.HTTP_406_NOT_ACCEPTABLE)
        
        used_qr_code = Entry.objects.filter(qr_code=qr_code.id).first()
        if used_qr_code:
            return Response(data={'result': 'This QR code is already used!'}, status=status.HTTP_409_CONFLICT)

        request.data['qr_code'] = qr_code.id
        request.data['user'] = request.user.id
        branch = request.user.branch
        request.data['branch'] = branch.id
        serializer = EntrySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            qr_code.used=True
            qr_code.save()
            
            print('valid data')
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        print(serializer.errors)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
