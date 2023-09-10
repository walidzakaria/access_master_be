from django.contrib import admin
from .models import QrCode, Entry

# Register your models here.
class QrCodeAdmin(admin.ModelAdmin):
    list_display = ('id', 'qr_code', )
    search_fields = ('id', 'qr_code', )


class EntryAdmin(admin.ModelAdmin):
    list_display = ('id', 'qr_code', 'entry_time', )
    search_fields = ('id', 'qr_code', 'entry_time', )
    readonly_fields = ('entry_time', )


admin.site.register(QrCode, QrCodeAdmin)
admin.site.register(Entry, EntryAdmin)