import datetime
from operator import mod

import django.utils.timezone
from django.core.validators import MaxValueValidator, MinValueValidator, MaxLengthValidator
from django.db import models
from django.db.models import CharField, PositiveBigIntegerField
from employee.validators import validate_file_extension
from .utils import COUNTRY_LIST, LEVEL

APPLICATION_STATUS = (
    ('N', 'New'),
    ('O', 'On-Hold'),
    ('R', 'Rejected'),
    ('B', 'Black-List'),
    ('A', 'Accepted'),
)


# Create your models here.
class Position(models.Model):
    position = models.CharField(max_length=50, unique=True, db_index=True)
    rank = models.PositiveSmallIntegerField()

    def __str__(self):
        return f'{self.position} ({self.rank})'
    
    class Meta:
        ordering = ('position',)


class ComputerSkill(models.Model):
    computer_skill = models.CharField(max_length=60, unique=True, db_index=True)

    class Meta:
        verbose_name_plural = 'Computer Skill'

    def __str__(self):
        return self.computer_skill


class Language(models.Model):
    language = models.CharField(max_length=20, unique=True, db_index=True)

    def __str__(self):
        return self.language


class Application(models.Model):
    objects = None
    user = models.ForeignKey('authapp.User', on_delete=models.CASCADE, null=True, blank=True)
    position = models.ForeignKey(Position, on_delete=models.CASCADE)
    issue_date = models.DateTimeField(auto_now_add=True)
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    SEX = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    sex = models.CharField(max_length=1, choices=SEX, db_index=True)
    date_of_birth = models.DateField(db_index=True)
    country_of_birth = models.CharField(max_length=2, choices=COUNTRY_LIST, default='EG')
    address = models.CharField(max_length=200)
    MARITAL_STATUS = (
        ('S', 'Single'),
        ('M', 'Married'),
        ('W', 'Widowed'),
        ('D', 'Divorced'),
        ('P', 'Separated'),
    )
    marital_status = models.CharField(max_length=1, choices=MARITAL_STATUS, default='S', db_index=True)
    has_children = models.BooleanField(default=False)
    mobile_number = models.CharField(max_length=11, db_index=True, unique=True)
    home_telephone_number = models.CharField(max_length=11, blank=True, null=True, )
    id_card_number = models.CharField(max_length=14, unique=True)
    id_date_of_issue = models.DateField()
    mother_name = models.CharField(max_length=150)
    RELIGION = (
        ('M', 'Muslim'),
        ('C', 'Christian'),
        ('O', 'Other'),
    )
    religion = models.CharField(max_length=1, choices=RELIGION)
    MILITARY_STATUS = (
        ('N', 'Not applicable'),
        ('C', 'Completed'),
        ('P', 'Postponed'),
        ('E', 'Exempted'),
    )
    military_status = models.CharField(max_length=1, choices=MILITARY_STATUS, default='C', db_index=True)
    military_obligations = models.BooleanField(default=False)
    permanent_resident = models.BooleanField(default=True)
    visa = models.CharField(max_length=200, blank=True, null=True, verbose_name='What visas do you hold')
    reference = models.CharField(max_length=200, blank=True, null=True, verbose_name='Who referred you to us')
    EMPLOYMENT_TYPE = (
        ('F', 'Full Time'),
        ('P', 'Part Time'),
        ('C', 'Casual')
    )
    employment_type = models.CharField(max_length=1, choices=EMPLOYMENT_TYPE, default='F', db_index=True)
    daily_working_hours = models.PositiveSmallIntegerField(
        default=8, verbose_name='Daily working hours you can work')
    can_work_night_shifts = models.BooleanField(default=True)
    when_can_you_start = models.DateField()
    HEALTH_STATUS = (
        ('E', 'Excellent'),
        ('G', 'Good'),
        ('F', 'Fair'),
    )
    general_health_status = models.CharField(max_length=1, choices=HEALTH_STATUS, default='G')
    do_you_smoke = models.BooleanField()
    medical_issues = models.TextField(
        null=True, blank=True, verbose_name='Medical issues conflict with duties')
    contact_name = models.CharField(max_length=150)
    contact_address = models.TextField(null=True, blank=True)
    contact_phone_number = models.CharField(max_length=11, validators=[MaxLengthValidator(11),
                                                                       MaxLengthValidator(11)])
    further_information = models.TextField(
        null=True, blank=True, verbose_name='Any further information you want to add')
    bank_payment = models.BooleanField(
        default=True, verbose_name='I agree to have my wages credited directly to a nominated bank account')
    driving_license = models.BooleanField(default=False)
    application_status = models.CharField(max_length=1, choices=APPLICATION_STATUS, default='N')
    remarks = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class ApplicationEducation(models.Model):
    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name='education')
    school = models.CharField(max_length=50, verbose_name='Name of school')
    degree = models.CharField(max_length=20)
    year = models.PositiveIntegerField(validators=[MinValueValidator(1984),
                                                   MaxValueValidator(datetime.date.today().year)])

    # @DONE: add years

    def __str__(self):
        return f'{self.school}: {self.degree}'


class ApplicationLanguages(models.Model):
    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name='languages')
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    speaking = models.CharField(max_length=1, choices=LEVEL, default='G', db_index=True)
    writing = models.CharField(max_length=1, choices=LEVEL, default='G', db_index=True)
    reading = models.CharField(max_length=1, choices=LEVEL, default='G', db_index=True)

    def __str__(self):
        return f'{self.language}: {self.speaking}-{self.writing}-{self.reading}'

    class Meta:
        verbose_name_plural = 'Application Languages'


class PreviousEmployment(models.Model):
    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name='employments')
    company = models.CharField(max_length=100, db_index=True, verbose_name='Previous company name')
    address = models.CharField(max_length=200, blank=True, null=True)
    position = models.CharField(max_length=100, db_index=True, verbose_name='Previous position')
    employed_from = models.DateField()
    employed_to = models.DateField()
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    job_description = models.TextField(null=True, blank=True)
    supervisor = models.CharField(max_length=150, blank=True, null=True, verbose_name='Immediate supervisor')
    supervisor_position = models.CharField(max_length=150, blank=True, null=True, verbose_name='Position of immediate '
                                                                                               'supervisor')
    reasons_for_leave = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.company}: {self.position}'


class References(models.Model):
    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name='references')
    name = models.CharField(max_length=50, verbose_name='Reference Name')
    address = models.CharField(max_length=50, verbose_name='Reference Address', blank=True, null=True)
    company = models.CharField(max_length=50, verbose_name='Reference Company', blank=True, null=True)
    position = models.CharField(max_length=50, verbose_name='Reference Position', blank=True, null=True)
    reference_phone_number = models.CharField(max_length=11, blank=True, null=True)

    class Meta:
        verbose_name_plural = 'References'

    def __str__(self):
        return f'{self.name}: {self.position}'


class OtherReferences(models.Model):
    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name='other_references', )
    name = models.CharField(max_length=50, verbose_name='Reference Name')
    address = models.CharField(max_length=50, verbose_name='Reference Address', blank=True, null=True)
    company = models.CharField(max_length=50, verbose_name='Reference Company', blank=True, null=True)
    position = models.CharField(max_length=50, verbose_name='Reference Position', blank=True, null=True)
    reference_phone_number = models.CharField(max_length=11, blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Other References'

    def __str__(self):
        return f'{self.name}: {self.position}'


class Test(models.Model):
    name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()

    def __str__(self):
        return self.name


class ApplicationStatus(models.Model):
    application = models.ForeignKey(Application, on_delete=models.CASCADE)
    issued_by = models.ForeignKey('authapp.User', on_delete=models.CASCADE)
    issue_date = models.DateTimeField(auto_now=True)
    application_status = models.CharField(max_length=1, choices=APPLICATION_STATUS, default='N')
    comments = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.application.first_name} {self.application.last_name}: {self.application_status}'

    class Meta:
        verbose_name_plural = 'Application Status'
        ordering = ('-issue_date',)

    def save(self, *args, **kwargs):
        application_to_update = self.application
        application_to_update.application_status = self.application_status
        application_to_update.remarks = self.comments
        application_to_update.save()
        print('updated')
        super(ApplicationStatus, self).save(*args, **kwargs)


class JobSection(models.Model):
    section = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.section


class Job(models.Model):
    job = models.CharField(max_length=250)
    LEVELS = (
        ('E', 'Entry-level'),
        ('I', 'Intermediate'),
        ('M', 'Mid-level'),
        ('S', 'Senior or executive-level')
    )
    level = models.CharField(max_length=1, choices=LEVELS, default='E', db_index=True)
    section = models.ForeignKey(JobSection, on_delete=models.CASCADE)
    post_date = models.DateField(default=django.utils.timezone.now)
    about = models.TextField(blank=True, null=True)
    job_description = models.TextField()
    qualifications = models.TextField()
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.job

    class Meta:
        ordering = ('-post_date',)


class Apply(models.Model):
    issue_date = models.DateTimeField(auto_created=True, db_index=True)
    full_name = models.CharField(max_length=250)
    mobile = models.CharField(max_length=12)
    email_address = models.EmailField()
    job = models.ForeignKey(Job, on_delete=models.CASCADE, blank=True, null=True)
    message = models.TextField(null=True, blank=True)
    resume = models.FileField(upload_to='resume', blank=True, null=True, validators=[validate_file_extension], )
    STATUS = (
        ('C', 'Yes, I am a current employee'),
        ('F', 'Yes, I am a former employee'),
        ('N', 'No'),
    )
    status = models.CharField(max_length=1, default='N',
                              choices=STATUS,
                              help_text='Are you a current or former Red Sea 24 company employee?')

    class Meta:
        verbose_name_plural = 'Apply Requests'
        ordering = ('-issue_date',)


class ContactUs(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Name: {self.name}, Email: {self.email}'

    class Meta:
        verbose_name_plural = 'Contact us'
        ordering = ('-date',)
