from django.shortcuts import render
from django.utils.datetime_safe import datetime
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def index(request):
    date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    message = f'Server is live current time is {date}!'
    return Response(data=message, status=status.HTTP_200_OK)


def index(request):
    return render(request, template_name='index.html')


def show_requests(request):
    return render(request, 'request.html')

def with_id(request, id):
    return render(request, 'index.html', {'id': id})

def with_title(request, title):
    return render(request, 'index.html', {'title': title})

def register(request, uid, token):
    return render(request, 'index.html', {'uid': uid, 'token': token})
    