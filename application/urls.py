from django.urls import path

from .views import (
    get_positions, get_languages, post_application, print_application, get_application,
    get_application_summary, get_tests, post_test, update_test, patch_test, delete_test,
    get_summarized_jobs, get_job, post_contact_us, post_job_request, suggest_jobs,
    put_application, get_application_status, post_application_status, get_computer_skill,
)


urlpatterns = [
    path('positions/', get_positions, name='positions'),
    path('languages/', get_languages, name='languages'),
    path('computer-skill/', get_computer_skill, name='computer-skill'),
    path('apply/', post_application, name='apply'),
    path('apply/edit/<int:application_id>/', put_application, name='application-edit'),
    path('print/<int:application_id>/', print_application, name='print-application'),
    path('<int:application_id>/', get_application, name='get-application'),
    path('application-status/<int:application_id>/', get_application_status, name='application-status'),
    path('application-status/', post_application_status, name='post-application-status'),
    path('summary/', get_application_summary, name='application-summary'),
    path('test/', get_tests, name='test'),
    path('test/create/', post_test, name='create-test'),
    path('test/update/<int:test_id>/', update_test, name='put-test'),
    path('test/patch/<int:test_id>/', patch_test, name='patch-test'),
    path('test/delete/<int:test_id>/', delete_test, name='delete-test'),

    path('jobs/', get_summarized_jobs, name='get-summarized-jobs'),
    path('job-suggestions/', suggest_jobs, name='get-job-suggestions'),
    path('job/<int:job_id>/', get_job, name='get-job'),
    path('job/post-resume/', post_job_request, name='post-resume'),
    path('contact-us/', post_contact_us, name='contact-us'),
]
