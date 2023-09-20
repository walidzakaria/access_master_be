from typing import Any
from django.contrib import admin
from .models import QrCode, Entry, Branch, PrintOrder

# Register your models here.
class QrCodeAdmin(admin.ModelAdmin):
    list_display = ('id', 'print_order', 'qr_code', 'used', )
    search_fields = ('id', 'qr_code', )
    list_filter = ('used', 'print_order', )


class EntryAdmin(admin.ModelAdmin):
    list_display = ('id', 'qr_code', 'entry_time', )
    search_fields = ('id', 'qr_code', 'entry_time', )
    readonly_fields = ('entry_time', )


class BranchAdmin(admin.ModelAdmin):
    list_display = ('id', 'branch', )
    search_fields = ('branch', )


class QrCodeInline(admin.TabularInline):
    model = QrCode
    extra = 0


class PrintOrderAdmin(admin.ModelAdmin):
    inlines = [QrCodeInline, ]
    readonly_fields = ('time', )
    list_display = ('id', 'time', )
    search_fields = ('id', )
    list_filter = ('time', )


admin.site.register(QrCode, QrCodeAdmin)
admin.site.register(Entry, EntryAdmin)
admin.site.register(Branch, BranchAdmin)
admin.site.register(PrintOrder, PrintOrderAdmin)

