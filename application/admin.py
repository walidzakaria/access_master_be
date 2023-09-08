from django.contrib import admin
from .models import Position, Application, ApplicationEducation, ApplicationLanguages, Language, PreviousEmployment, \
    References, OtherReferences, Job, JobSection, Apply, ContactUs, ApplicationStatus, ComputerSkill


# Register your models here.
class PositionAdmin(admin.ModelAdmin):
    list_display = ('position', 'rank',)
    search_fields = ('position',)
    list_filter = ('rank',)


class ApplicationEducationAdmin(admin.TabularInline):
    model = ApplicationEducation


class JobAdmin(admin.ModelAdmin):
    list_display = ('job', 'id', 'level', 'section', 'post_date', 'active',)
    search_fields = ('job', )
    list_filter = ('section', 'level', 'active',)


class JobSectionAdmin(admin.ModelAdmin):
    list_display = ('id', 'section',)
    search_fields = ('section',)


class ApplicationStatusAdmin(admin.ModelAdmin):
    list_display = ('id', 'application', 'issued_by', 'issue_date', 'application_status', 'comments',)
    list_filter = ('application_status',)
    readonly_fields = ('issue_date',)


class ApplicationLanguagesAdmin(admin.TabularInline):
    model = ApplicationLanguages


class LanguageAdmin(admin.ModelAdmin):
    list_display = ('language',)
    search_fields = ('language',)


class ComputerSkillAdmin(admin.ModelAdmin):
    list_display = ('computer_skill', )
    search_fields = ('computer_skill',)


class ApplicationEmploymentHistoryAdmin(admin.TabularInline):
    model = PreviousEmployment


class ReferencesAdmin(admin.TabularInline):
    model = References


class OtherReferencesAdmin(admin.TabularInline):
    model = OtherReferences


class ApplicationAdmin(admin.ModelAdmin):
    inlines = [ApplicationEducationAdmin, ApplicationLanguagesAdmin, ApplicationEmploymentHistoryAdmin,
               ReferencesAdmin, OtherReferencesAdmin, ]
    list_display = ('id', 'first_name', 'middle_name', 'last_name')
    search_fields = ('first_name', 'middle_name', 'last_name',)
    readonly_fields = ('issue_date',)

    fieldsets = (
        ('Personal Info', {
            'fields': (
                'user', 'position', 'issue_date', 'first_name', 'middle_name', 'last_name', 'sex', 'date_of_birth',
                'country_of_birth', 'address', 'marital_status', 'has_children',
                'mobile_number', 'home_telephone_number',
                'id_card_number', 'id_date_of_issue', 'mother_name', 'religion', 'military_status',
                'military_obligations',
                'permanent_resident', 'visa', 'reference', 'driving_license',),
            'classes': ('collapse',), }),
        ('Employment Sought', {
            'fields': (
                'employment_type', 'daily_working_hours',
                'can_work_night_shifts', 'when_can_you_start',),
            'classes': ('collapse',),
        },),
        ('Medical Information', {
            'fields': (
                'general_health_status', 'do_you_smoke',
                'medical_issues',),
            'classes': ('collapse',),
        },),
        ('Emergency Contact', {
            'fields': ('contact_name', 'contact_address', 'contact_phone_number',),
            'classes': ('collapse',),
        },),
        ('Additional Information', {
            'fields': ('further_information',),
            'classes': ('collapse',),
        },),
        ('Application Status', {
            'fields': ('application_status', 'remarks',),
            'classes': ('collapse',),
        },),
        ('Direct Payment', {
            'fields': ('bank_payment',),
            'classes': ('collapse',),
        },),
    )


class ApplyAdmin(admin.ModelAdmin):
    list_display = ('id', 'issue_date', 'full_name', 'email_address', 'job', 'resume', 'status',)
    search_fields = ('full_name', 'email_address', 'job__job',)
    list_filter = ('status',)


class ContactUsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'subject', 'message', 'date',)
    search_fields = ('name', 'email', 'subject', 'message',)
    list_filter = ('date',)


admin.site.register(Position, PositionAdmin)
# admin.site.register(PickupPoint, PickupPointAdmin)
admin.site.register(Application, ApplicationAdmin)
admin.site.register(Language, LanguageAdmin)
admin.site.register(ComputerSkill, ComputerSkillAdmin)
admin.site.register(Job, JobAdmin)
admin.site.register(JobSection, JobSectionAdmin)
admin.site.register(Apply, ApplyAdmin)
admin.site.register(ContactUs, ContactUsAdmin)
admin.site.register(ApplicationStatus, ApplicationStatusAdmin)
