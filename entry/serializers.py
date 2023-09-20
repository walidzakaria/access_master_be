from rest_framework import serializers

from entry.utils import get_local_date

from .models import Branch, QrCode, Entry
from django.conf import settings


class QrCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = QrCode
        fields = '__all__'



class EntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Entry
        fields = '__all__'


class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = '__all__'


class BranchEntriesSerializer(serializers.ModelSerializer):
    entries = serializers.SerializerMethodField()

    def get_entries(self, obj):
        local_now = get_local_date(settings.TIME_ZONE)
        print(local_now)
        entries = Entry.objects.filter(
            branch=obj,
            entry_time__date=local_now
            ).count()
        return entries
    
    class Meta:
        model = Branch
        fields = '__all__'

