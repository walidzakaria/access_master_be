# from django.contrib.sites import requests
from datetime import tzinfo
from django.utils import timezone
import pytz
import requests
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.parsers import FileUploadParser, MultiPartParser, FormParser
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, views, status
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from djoser.conf import django_settings
from django.forms.models import model_to_dict

from .models import (
    ApplicationStatus, JobSection, Position, Language, Application, PreviousEmployment, Test, Job,
    References, OtherReferences, Apply, ApplicationEducation, ApplicationLanguages, ComputerSkill, )
from .serializers import (
    ApplicationStatusSerializer, PositionSerializer, LanguageSerializer, ApplicationSerializer,
    ApplicationEducationSerializer,
    ApplicationLanguagesSerializer, PreviousEmploymentSerializer,
    ApplicationDetailedSerializer, SummarizedApplicationSerializer,
    TestSerializer, SummarizedJobSerializer, JobSerializer, ApplicationLanguagesEditSerializer,
    ReferencesSerializer, OtherReferencesSerializer, ApplySerializer, ContactUsSerializer,
    ApplicationStatusEditSerializer, ComputerSkillSerializer,
)
from .utils import doc_application, send_message, send_resume, send_confirmation


# Create your views here.
@api_view(['GET'])
def get_positions(request):
    """List all positions"""

    if request.method == 'GET':
        positions = Position.objects.order_by('position').all()
        serializer = PositionSerializer(positions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_languages(request):
    """List all languages"""

    if request.method == 'GET':
        languages = Language.objects.order_by('language').all()
        serializer = LanguageSerializer(languages, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_computer_skill(request):
    """List all computer skills"""

    if request.method == 'GET':
        computer_skill = ComputerSkill.objects.order_by('computer_skill').all()
        serializer = ComputerSkillSerializer(computer_skill, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def post_application(request):
    """Create new application"""

    if request.method == 'POST':
        # check if the ID is previously added
        application_id = request.data['applicationInfo']['id_card_number']
        applicant_with_same_id = Application.objects.filter(id_card_number=application_id).first()
        if applicant_with_same_id:
            return Response(data={'error_type': 'id card number'}, status=status.HTTP_406_NOT_ACCEPTABLE)

        # check if the mobile is previously added
        mobile_number = request.data['applicationInfo']['mobile_number']
        applicant_with_same_mobile = Application.objects.filter(mobile_number=mobile_number).first()
        if applicant_with_same_mobile:
            return Response(data={'error_type': 'mobile number'}, status=status.HTTP_406_NOT_ACCEPTABLE)

        app_serializer = ApplicationSerializer(data=request.data['applicationInfo'])
        if app_serializer.is_valid():
            app_serializer.save()

            # include applicant id into sub tables
            applicant_id = app_serializer.data['id']
            for education in request.data['educations']:
                education['application'] = applicant_id
            for language in request.data['languages']:
                language['application'] = applicant_id
            for job in request.data['prevJobs']:
                job['application'] = applicant_id
            print(request.data)
            for ref in request.data['references']:
                ref['application'] = applicant_id
            for ref in request.data['otherReferences']:
                ref['application'] = applicant_id

            # save educations
            education_serializer = ApplicationEducationSerializer(data=request.data['educations'], many=True)
            if education_serializer.is_valid():
                education_serializer.save()
            else:
                print('education errors', education_serializer.errors)

            # save languages
            language_serializer = ApplicationLanguagesEditSerializer(data=request.data['languages'], many=True)
            if language_serializer.is_valid():
                language_serializer.save()
            else:
                print('language errors', language_serializer.errors)

            # save prev employments
            employment_serializer = PreviousEmploymentSerializer(data=request.data['prevJobs'], many=True)
            print(request.data['prevJobs'])
            if employment_serializer.is_valid():
                employment_serializer.save()
                # print(employment_serializer.data)
            else:
                print('employment errors', employment_serializer.errors)

            # save references
            references_serializer = ReferencesSerializer(data=request.data['references'], many=True)
            if references_serializer.is_valid():
                references_serializer.save()
            else:
                print('references errors', references_serializer.errors)

            # save other references
            other_references_serializer = OtherReferencesSerializer(data=request.data['otherReferences'], many=True)
            if other_references_serializer.is_valid():
                other_references_serializer.save()
            else:
                print('other references errors', other_references_serializer.errors)

            return Response(app_serializer.data, status=status.HTTP_201_CREATED)
        print(app_serializer.errors)
        return Response(app_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
def put_application(request, application_id):
    """Update application by ID"""

    if request.method == 'PUT':

        # check if application doesn't exist
        application_to_edit = Application.objects.filter(id=application_id).first()
        if not application_to_edit:
            return Response(data={'message': 'no records'}, status=status.HTTP_204_NO_CONTENT)

        # check if the ID is previously added to a different app
        card_number = request.data['applicationInfo']['id_card_number']
        applicant_with_same_id = Application.objects.filter(
            id_card_number=card_number,
            ).exclude(id=application_id).first()

        if applicant_with_same_id:
            return Response(data={'error_type': 'id card number'}, status=status.HTTP_406_NOT_ACCEPTABLE)

        # check if the mobile is previously added
        mobile_number = request.data['applicationInfo']['mobile_number']
        applicant_with_same_mobile = Application.objects.filter(
            mobile_number=mobile_number).exclude(id=application_id).first()
        if applicant_with_same_mobile:
            return Response(data={'error_type': 'mobile number'}, status=status.HTTP_406_NOT_ACCEPTABLE)

        app_serializer = ApplicationSerializer(application_to_edit, data=request.data['applicationInfo'])
        if app_serializer.is_valid():
            app_serializer.update(application_to_edit, app_serializer.validated_data)

            # include applicant id into sub tables
            for education in request.data['educations']:
                education['application'] = application_id
            for language in request.data['languages']:
                language['application'] = application_id
            for job in request.data['prevJobs']:
                job['application'] = application_id
            print(request.data)
            for ref in request.data['references']:
                ref['application'] = application_id
            for ref in request.data['otherReferences']:
                ref['application'] = application_id

            # save educations
            prev_educations = ApplicationEducation.objects.filter(application__id=application_id).all()
            prev_educations.delete()
            education_serializer = ApplicationEducationSerializer(data=request.data['educations'], many=True)
            if education_serializer.is_valid():
                education_serializer.save()
            else:
                print('education errors', education_serializer.errors)

            # save languages
            prev_languages = ApplicationLanguages.objects.filter(application__id=application_id).all()
            prev_languages.delete()
            language_serializer = ApplicationLanguagesEditSerializer(data=request.data['languages'], many=True)
            if language_serializer.is_valid():
                language_serializer.save()
            else:
                print('language errors', language_serializer.errors)

            # save prev employments
            prev_employments = PreviousEmployment.objects.filter(application__id=application_id).all()
            prev_employments.delete()
            employment_serializer = PreviousEmploymentSerializer(data=request.data['prevJobs'], many=True)
            print(request.data['prevJobs'])
            if employment_serializer.is_valid():
                employment_serializer.save()
            else:
                print('employment errors', employment_serializer.errors)

            # save references
            prev_references = References.objects.filter(application__id=application_id).all()
            prev_references.delete()
            references_serializer = ReferencesSerializer(data=request.data['references'], many=True)
            if references_serializer.is_valid():
                references_serializer.save()
            else:
                print('references errors', references_serializer.errors)

            # save other references
            prev_other_references = OtherReferences.objects.filter(application__id=application_id).all()
            prev_other_references.delete()
            print('other references:', request.data['otherReferences'])
            other_references_serializer = OtherReferencesSerializer(data=request.data['otherReferences'], many=True)
            if other_references_serializer.is_valid():
                other_references_serializer.save()
            else:
                print('other references errors', other_references_serializer.errors)
            return Response(app_serializer.data, status=status.HTTP_200_OK)
        return Response(app_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def print_application(request, application_id):
    # @TODO: add references & other references to docx template
    # application = Application.objects.select_related('position').get(pk=application_id)
    application = Application.objects.get(pk=application_id)
    if application:
        serializer = ApplicationDetailedSerializer(application)
        context = serializer.data
        print(context)
        export_name = f'{application.first_name}_{application.last_name}'
        return doc_application(request, context, export_name)


@api_view(['GET', ])
# @TODO: add auth & permissions
def get_application(request, application_id):
    """Show detailed application"""
    if request.method == 'GET':
        application = Application.objects.filter(id=application_id).first()
        if not application:
            return Response(data={'message': 'no records'}, status=status.HTTP_204_NO_CONTENT)
        serializer = ApplicationDetailedSerializer(application)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET', ])
# @TODO: add auth & permissions
def get_application_summary(request):
    """List summarized applications"""
    if request.method == 'GET':
        applications = Application.objects.all()
        serializer = SummarizedApplicationSerializer(applications, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET', ])
# @permission_classes([IsAuthenticated])
def get_tests(request):
    """List all tests"""
    if request.method == 'GET':
        test = Test.objects.all()
        serializer = TestSerializer(test, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


@api_view(['POST', ])
def post_test(request):
    """Post a new test"""
    if request.method == 'POST':
        serializer = TestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT', ])
@permission_classes([IsAuthenticated])
def update_test(request, test_id):
    """Update a test using ID"""
    if request.method == 'PUT':
        user = request.user
        print(user)
        test_to_update = Test.objects.filter(id=test_id).first()
        if not test_to_update:
            return Response(data={'message': 'no records'}, status=status.HTTP_204_NO_CONTENT)

        serializer = TestSerializer(test_to_update, data=request.data)
        if serializer.is_valid():
            serializer.update(test_to_update, serializer.validated_data)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PATCH', ])
@permission_classes([IsAuthenticated])
def patch_test(request, test_id):
    """Update a test name by ID"""
    if request.method == 'PATCH':
        if 'age' not in request.data:
            return Response(data={'message': 'missing age'}, status=status.HTTP_400_BAD_REQUEST)
        age = request.data['age']
        test_to_update = Test.objects.filter(id=test_id).first()
        if not test_to_update:
            return Response(data={'message': 'no records'}, status=status.HTTP_204_NO_CONTENT)

        test_to_update.age = age
        test_to_update.save()
        return Response(data={'message': 'saved'}, status=status.HTTP_200_OK)


@api_view(['DELETE', ])
@permission_classes([IsAuthenticated])
def delete_test(request, test_id):
    """Delete a test name by ID"""
    if request.method == 'DELETE':
        test_to_delete = Test.objects.filter(id=test_id).first()
        if not test_to_delete:
            return Response(data={'message': 'no records'}, status=status.HTTP_204_NO_CONTENT)

        test_to_delete.delete()
        return Response(data={'message': 'deleted'}, status=status.HTTP_200_OK)


# Job Suggestions Search
@api_view(['GET'])
def suggest_jobs(request):
    """Suggest jobs"""

    if request.method == 'GET':
        result = []
        jobs = Job.objects.filter(active=True).values('job').all()
        result = [j['job'] for j in jobs]

        sections = JobSection.objects.all()
        for s in sections:
            result.append(s.section)

        result.sort()

    return Response(data={'result': result}, status=status.HTTP_200_OK)


@api_view(['GET', ])
def get_summarized_jobs(request):
    """List all valid jobs summarized"""
    if request.method == 'GET':
        jobs = Job.objects.filter(active=True).all()
        serializer = SummarizedJobSerializer(jobs, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


@api_view(['GET', ])
def get_job(request, job_id):
    """Show job details by id"""
    if request.method == 'GET':
        job = Job.objects.filter(id=job_id).first()
        serializer = JobSerializer(job)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


@api_view(['POST', ])
def post_job_request(request):
    """Post application request"""
    if request.method == 'POST':

        parser_classes = (MultiPartParser, FormParser,)
        request_data = request.data
        request_data._mutable = True
        request_data['issue_date'] = timezone.now()
        serializer = ApplySerializer(data=request.data)
        # resume = request.FILES.getlist('resume')[0]
        if serializer.is_valid():
            info = serializer.save()
            job = info.job
            job_status = info.get_status_display()
            print('sending form')
            send_resume(info.full_name, info.mobile, info.email_address, job_status,
                        info.resume.path, info.message, job.job)
            print('sending confirmation')
            confirm_email = send_confirmation(info.full_name, info.email_address, job.job)
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        print('sending errors')
        print(serializer.errors)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST', ])
def post_contact_us(request):
    """Send contact us message"""
    print('receiving request', request.data)
    if request.method == 'POST':

        serializer = ContactUsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            result = send_message(serializer.data['name'], serializer.data['email'],
                                  serializer.data['subject'], serializer.data['message'])
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        print(serializer.errors)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', ])
def get_application_status(request, application_id):
    """List all application status history"""
    if request.method == 'GET':
        application = Application.objects.filter(id=application_id).first()
        if not application:
            return Response(data={'result': 'no data'}, status=status.HTTP_204_NO_CONTENT)
        
        application_info = {
            'full_name': f'{application.first_name} {application.last_name}',
            'issue_date': application.issue_date,
        }
        application_status = ApplicationStatus.objects.filter(application=application_id).all()
        
        if application_status.count() > 0:
            serializer = ApplicationStatusSerializer(application_status, many=True)
            application_info['status'] = serializer.data
        else:
            application_info['status'] = []
        
        return Response(data=application_info, status=status.HTTP_200_OK)


@api_view(['POST', ])
@permission_classes([IsAuthenticated])
def post_application_status(request):
    """Create new status for an application"""
    if request.method == 'POST':
        user = request.user
        request.data['issued_by'] = user.id
        serializer = ApplicationStatusEditSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)