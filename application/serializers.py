import datetime

from rest_framework import serializers
from .utils import COUNTRY_LIST, LEVEL

from authapp.models import User
from .models import (
    Position, Language, Application, ApplicationEducation,
    ApplicationLanguages, PreviousEmployment, Test, Job, JobSection,
    References, OtherReferences, Apply, ContactUs,
    ApplicationStatus, ComputerSkill,
)
from employee.models import Employee


class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = '__all__'


class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = '__all__'


class ComputerSkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComputerSkill
        fields = '__all__'


class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = '__all__'


class ApplicationEducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicationEducation
        fields = '__all__'


class ApplicationLanguagesEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicationLanguages
        fields = '__all__'


class ApplicationLanguagesSerializer(serializers.ModelSerializer):
    language = LanguageSerializer(read_only=True)
    speaking_level = serializers.SerializerMethodField()
    writing_level = serializers.SerializerMethodField()
    reading_level = serializers.SerializerMethodField()

    def get_speaking_level(self, obj):
        return dict(LEVEL)[obj.speaking]

    def get_writing_level(self, obj):
        return dict(LEVEL)[obj.writing]

    def get_reading_level(self, obj):
        return dict(LEVEL)[obj.reading]

    class Meta:
        model = ApplicationLanguages
        fields = '__all__'


class PreviousEmploymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PreviousEmployment
        fields = '__all__'


class SummarizedApplicationSerializer(serializers.ModelSerializer):
    position = PositionSerializer(read_only=True)

    class Meta:
        model = Application
        fields = ('id', 'issue_date', 'first_name', 'last_name', 'position', 'user')


class ReferencesSerializer(serializers.ModelSerializer):
    class Meta:
        model = References
        fields = '__all__'


class OtherReferencesSerializer(serializers.ModelSerializer):
    class Meta:
        model = OtherReferences
        fields = '__all__'


class ApplicationDetailedSerializer(serializers.ModelSerializer):
    position = PositionSerializer(read_only=True)
    education = ApplicationEducationSerializer(read_only=True, many=True)
    languages = ApplicationLanguagesSerializer(read_only=True, many=True)
    employments = PreviousEmploymentSerializer(read_only=True, many=True)
    references = ReferencesSerializer(read_only=True, many=True)
    other_references = OtherReferencesSerializer(read_only=True, many=True)
    issue_date_trimmed = serializers.SerializerMethodField()
    country_name = serializers.SerializerMethodField()
    id_issue_date = serializers.SerializerMethodField()
    start_date = serializers.SerializerMethodField()

    def get_issue_date_trimmed(self, obj):
        return obj.issue_date.date().strftime('%Y/%m/%d')

    def get_country_name(self, obj):
        return dict(COUNTRY_LIST)[obj.country_of_birth]

    def get_id_issue_date(self, obj):
        return obj.id_date_of_issue.strftime('%B-%Y')

    def get_start_date(self, obj):
        return obj.when_can_you_start.strftime('%Y/%m/%d')

    class Meta:
        model = Application
        fields = '__all__'


class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = '__all__'


class JobSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobSection
        fields = '__all__'


class SummarizedJobSerializer(serializers.ModelSerializer):
    section = JobSectionSerializer(read_only=True)

    class Meta:
        model = Job
        fields = ('id', 'section', 'level', 'job', 'post_date', 'about',)


class JobSerializer(serializers.ModelSerializer):
    section = JobSectionSerializer(read_only=True)

    class Meta:
        model = Job
        fields = '__all__'


class UserApplicationDetailsSerializer(serializers.ModelSerializer):
    user_application = ApplicationDetailedSerializer(read_only=True)

    class Meta:
        model = User
        fields = '__all__'


class ApplySerializer(serializers.ModelSerializer):
    class Meta:
        model = Apply
        fields = '__all__'


class ContactUsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactUs
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name',)


class ApplicationStatusSerializer(serializers.ModelSerializer):
    issued_by = UserSerializer()

    class Meta:
        model = ApplicationStatus
        fields = '__all__'


class ApplicationStatusEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicationStatus
        fields = '__all__'
