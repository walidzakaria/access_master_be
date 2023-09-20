from django.urls import path, include, re_path
from .views import create_qrs, post_entry, get_daily_entries, get_branches, get_branches_entries

urlpatterns = [
    path('create/', create_qrs, name='create-qrs'),
    path('enter/', post_entry, name='post-entry'),
    path('branches/', get_branches, name='get-branches'),
    path('branch-entries/', get_branches_entries, name='branch-entries'),
    path('daily-entries/<int:branch_id>/', get_daily_entries, name='get-daily-enties'),
]