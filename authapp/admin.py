from django.contrib import admin
from .models import User
from .forms import UserForm


# Register your models here.
class AdminUser(admin.ModelAdmin):
    form = UserForm
    list_display = ('username', 'email', 'first_name', 'last_name', 'branch', )
    search_fields = ('username', 'email', )

    # make user password read only if being edited
    def get_readonly_fields(self, request, obj=None):
        if obj:  # editing an existing object
            return self.readonly_fields + ('password',)
        return self.readonly_fields

    def save_model(self, request, obj, form, change):
        if not change:
            obj.set_password(obj.password)
        obj.save()


admin.site.register(User, AdminUser)
