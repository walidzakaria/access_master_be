# Generated by Django 4.0.1 on 2022-04-27 07:23

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import employee.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Application',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('issue_date', models.DateTimeField(auto_now_add=True)),
                ('first_name', models.CharField(max_length=50)),
                ('middle_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('sex', models.CharField(choices=[('M', 'Male'), ('F', 'Female')], db_index=True, max_length=1)),
                ('date_of_birth', models.DateField(db_index=True)),
                ('country_of_birth', models.CharField(choices=[('EG', 'EGYPT'), ('SA', 'SAUDI ARABIA'), ('KW', 'KUWAIT'), ('AE', 'UNITED ARAB EMIRATES'), ('AF', 'AFGHANISTAN'), ('AL', 'ALBANIA'), ('DZ', 'ALGERIA'), ('AS', 'AMERICAN SAMOA'), ('AD', 'ANDORRA'), ('AO', 'ANGOLA'), ('AR', 'ARGENTINA'), ('AM', 'ARMENIA'), ('AW', 'ARUBA'), ('AU', 'AUSTRALIA'), ('AT', 'AUSTRIA'), ('AZ', 'AZERBAIJAN'), ('BS', 'BAHAMAS'), ('BH', 'BAHRAIN'), ('BD', 'BANGLADESH'), ('BB', 'BARBADOS'), ('BY', 'BELARUS'), ('BE', 'BELGIUM'), ('BZ', 'BELIZE'), ('BJ', 'BENIN'), ('BM', 'BERMUDA'), ('BT', 'BHUTAN'), ('BO', 'BOLIVIA'), ('BA', 'BOSNIA'), ('BW', 'BOTSWANA'), ('BV', 'BOUVET ISLAND'), ('BR', 'BRAZIL'), ('BG', 'BULGARIA'), ('BF', 'BURKINA FASO'), ('BI', 'BURUNDI'), ('KH', 'CAMBODIA'), ('CM', 'CAMEROON'), ('CA', 'CANADA'), ('CV', 'CAPE VERDE'), ('KY', 'CAYMAN ISLANDS'), ('TD', 'CHAD'), ('CL', 'CHILE'), ('CN', 'CHINA'), ('CX', 'CHRISTMAS ISLAND'), ('CO', 'COLOMBIA'), ('KM', 'COMOROS'), ('CG', 'CONGO'), ('CR', 'COSTA RICA'), ('CI', 'CÔTE D'), ('HR', 'CROATIA'), ('CU', 'CUBA'), ('CY', 'CYPRUS'), ('CZ', 'CZECH REPUBLIC'), ('DK', 'DENMARK'), ('DJ', 'DJIBOUTI'), ('DM', 'DOMINICA'), ('DO', 'DOMINICAN REPUBLIC'), ('EC', 'ECUADOR'), ('SV', 'EL SALVADOR'), ('GQ', 'EQUATORIAL GUINEA'), ('ER', 'ERITREA'), ('EE', 'ESTONIA'), ('ET', 'ETHIOPIA'), ('FK', 'FALKLAND ISLANDS (MALVINAS)'), ('FO', 'FAROE ISLANDS'), ('FJ', 'FIJI'), ('FI', 'FINLAND'), ('FR', 'FRANCE'), ('GF', 'FRENCH GUIANA'), ('GA', 'GABON'), ('GM', 'GAMBIA'), ('GE', 'GEORGIA'), ('DE', 'GERMANY'), ('GH', 'GHANA'), ('GI', 'GIBRALTAR'), ('GR', 'GREECE'), ('GL', 'GREENLAND'), ('GD', 'GRENADA'), ('GP', 'GUADELOUPE'), ('GU', 'GUAM'), ('GT', 'GUATEMALA'), ('GN', 'GUINEA'), ('GY', 'GUYANA'), ('HT', 'HAITI'), ('HN', 'HONDURAS'), ('HK', 'HONG KONG'), ('HU', 'HUNGARY'), ('IS', 'ICELAND'), ('IN', 'INDIA'), ('ID', 'INDONESIA'), ('IR', 'IRAN'), ('IQ', 'IRAQ'), ('IE', 'IRELAND'), ('IL', 'ISRAEL'), ('IT', 'ITALY'), ('JM', 'JAMAICA'), ('JP', 'JAPAN'), ('JO', 'JORDAN'), ('KZ', 'KAZAKHSTAN'), ('KE', 'KENYA'), ('KI', 'KIRIBATI'), ('KP', 'KOREA'), ('KG', 'KYRGYZSTAN'), ('LV', 'LATVIA'), ('LB', 'LEBANON'), ('LS', 'LESOTHO'), ('LR', 'LIBERIA'), ('LY', 'LIBYA'), ('LI', 'LIECHTENSTEIN'), ('LT', 'LITHUANIA'), ('LU', 'LUXEMBOURG'), ('MO', 'MACAO'), ('MK', 'MACEDONIA'), ('MG', 'MADAGASCAR'), ('MW', 'MALAWI'), ('MY', 'MALAYSIA'), ('MV', 'MALDIVES'), ('ML', 'MALI'), ('MT', 'MALTA'), ('MQ', 'MARTINIQUE'), ('MR', 'MAURITANIA'), ('MU', 'MAURITIUS'), ('YT', 'MAYOTTE'), ('MX', 'MEXICO'), ('FM', 'MICRONESIA'), ('MD', 'MOLDOVA'), ('MC', 'MONACO'), ('MN', 'MONGOLIA'), ('ME', 'MONTENEGRO'), ('MS', 'MONTSERRAT'), ('MA', 'MOROCCO'), ('MZ', 'MOZAMBIQUE'), ('MM', 'MYANMAR'), ('NA', 'NAMIBIA'), ('NR', 'NAURU'), ('NP', 'NEPAL'), ('NL', 'NETHERLANDS'), ('NC', 'NEW CALEDONIA'), ('NZ', 'NEW ZEALAND'), ('NI', 'NICARAGUA'), ('NE', 'NIGER'), ('NG', 'NIGERIA'), ('NU', 'NIUE'), ('NF', 'NORFOLK ISLAND'), ('NO', 'NORWAY'), ('OM', 'OMAN'), ('PK', 'PAKISTAN'), ('PW', 'PALAU'), ('PS', 'PALESTINE'), ('PA', 'PANAMA'), ('PY', 'PARAGUAY'), ('PE', 'PERU'), ('PH', 'PHILIPPINES'), ('PN', 'PITCAIRN'), ('PL', 'POLAND'), ('PT', 'PORTUGAL'), ('PR', 'PUERTO RICO'), ('QA', 'QATAR'), ('RE', 'RÉUNION'), ('RO', 'ROMANIA'), ('RU', 'RUSSIAN FEDERATION'), ('RW', 'RWANDA'), ('SH', 'SAINT HELENA'), ('LC', 'SAINT LUCIA'), ('WS', 'SAMOA'), ('SM', 'SAN MARINO'), ('SN', 'SENEGAL'), ('RS', 'SERBIA'), ('SC', 'SEYCHELLES'), ('SL', 'SIERRA LEONE'), ('SG', 'SINGAPORE'), ('SK', 'SLOVAKIA'), ('SI', 'SLOVENIA'), ('SB', 'SOLOMON ISLANDS'), ('SO', 'SOMALIA'), ('ZA', 'SOUTH AFRICA'), ('SS', 'SOUTH SUDAN'), ('ES', 'SPAIN'), ('LK', 'SRI LANKA'), ('SD', 'SUDAN'), ('SR', 'SURINAME'), ('SZ', 'SWAZILAND'), ('SE', 'SWEDEN'), ('CH', 'SWITZERLAND'), ('SY', 'SYRIAN ARAB REPUBLIC'), ('TW', 'TAIWAN'), ('TJ', 'TAJIKISTAN'), ('TZ', 'TANZANIA'), ('TH', 'THAILAND'), ('TL', 'TIMOR-LESTE'), ('TG', 'TOGO'), ('TK', 'TOKELAU'), ('TO', 'TONGA'), ('TT', 'TRINIDAD AND TOBAGO'), ('TN', 'TUNISIA'), ('TR', 'TURKEY'), ('TM', 'TURKMENISTAN'), ('TV', 'TUVALU'), ('UG', 'UGANDA'), ('UA', 'UKRAINE'), ('GB', 'UNITED KINGDOM'), ('US', 'UNITED STATES'), ('UY', 'URUGUAY'), ('UZ', 'UZBEKISTAN'), ('VU', 'VANUATU'), ('VE', 'VENEZUELA'), ('VN', 'VIET NAM'), ('YE', 'YEMEN'), ('ZM', 'ZAMBIA'), ('ZW', 'ZIMBABWE')], default='EG', max_length=2)),
                ('address', models.CharField(max_length=200)),
                ('marital_status', models.CharField(choices=[('S', 'Single'), ('M', 'Married'), ('W', 'Widowed'), ('D', 'Divorced'), ('P', 'Separated')], db_index=True, default='S', max_length=1)),
                ('mobile_number', models.CharField(db_index=True, max_length=11, unique=True)),
                ('home_telephone_number', models.CharField(blank=True, max_length=11, null=True)),
                ('id_card_number', models.CharField(max_length=14, unique=True)),
                ('id_date_of_issue', models.DateField()),
                ('military_status', models.CharField(choices=[('N', 'Not applicable'), ('C', 'Completed'), ('P', 'Postponed'), ('E', 'Exempted')], db_index=True, default='C', max_length=1)),
                ('military_obligations', models.BooleanField(default=False)),
                ('permanent_resident', models.BooleanField(default=True)),
                ('visa', models.CharField(blank=True, max_length=200, null=True, verbose_name='What visas do you hold')),
                ('reference', models.CharField(blank=True, max_length=200, null=True, verbose_name='Who referred you to us')),
                ('employment_type', models.CharField(choices=[('F', 'Full Time'), ('P', 'Part Time'), ('C', 'Casual')], db_index=True, default='F', max_length=1)),
                ('daily_working_hours', models.PositiveSmallIntegerField(default=8, verbose_name='Daily working hours you can work')),
                ('can_work_night_shifts', models.BooleanField(default=True)),
                ('when_can_you_start', models.DateField()),
                ('general_health_status', models.CharField(choices=[('E', 'Excellent'), ('G', 'Good'), ('F', 'Fair')], default='G', max_length=1)),
                ('do_you_smoke', models.BooleanField()),
                ('medical_issues', models.TextField(blank=True, null=True, verbose_name='Medical issues conflict with duties')),
                ('contact_name', models.CharField(max_length=150)),
                ('contact_address', models.TextField(blank=True, null=True)),
                ('contact_phone_number', models.CharField(max_length=11, validators=[django.core.validators.MaxLengthValidator(11), django.core.validators.MaxLengthValidator(11)])),
                ('further_information', models.TextField(blank=True, null=True, verbose_name='Any further information you want to add')),
                ('bank_payment', models.BooleanField(default=True, verbose_name='I agree to have my wages credited directly to a nominated bank account')),
                ('driving_license', models.BooleanField(default=False)),
                ('application_status', models.CharField(choices=[('N', 'New'), ('O', 'On-Hold'), ('R', 'Rejected'), ('B', 'Black-List'), ('A', 'Accepted')], default='N', max_length=1)),
                ('remarks', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('job', models.CharField(max_length=250)),
                ('level', models.CharField(choices=[('E', 'Entry-level'), ('I', 'Intermediate'), ('M', 'Mid-level'), ('S', 'Senior or executive-level')], db_index=True, default='E', max_length=1)),
                ('post_date', models.DateField(default=django.utils.timezone.now)),
                ('about', models.TextField(blank=True, null=True)),
                ('active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='JobSection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('section', models.CharField(max_length=200, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language', models.CharField(db_index=True, max_length=20, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Position',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.CharField(db_index=True, max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Test',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('age', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='References',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Reference Name')),
                ('address', models.CharField(blank=True, max_length=50, null=True, verbose_name='Reference Address')),
                ('company', models.CharField(blank=True, max_length=50, null=True, verbose_name='Reference Company')),
                ('position', models.CharField(blank=True, max_length=50, null=True, verbose_name='Reference Position')),
                ('reference_phone_number', models.CharField(blank=True, max_length=11, null=True)),
                ('application', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='references', to='application.application')),
            ],
            options={
                'verbose_name_plural': 'References',
            },
        ),
        migrations.CreateModel(
            name='PreviousEmployment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company', models.CharField(db_index=True, max_length=100, verbose_name='Previous company name')),
                ('address', models.CharField(blank=True, max_length=200, null=True)),
                ('position', models.CharField(db_index=True, max_length=100, verbose_name='Previous position')),
                ('employed_from', models.DateField()),
                ('employed_to', models.DateField()),
                ('salary', models.DecimalField(decimal_places=2, max_digits=10)),
                ('job_description', models.TextField(blank=True, null=True)),
                ('supervisor', models.CharField(blank=True, max_length=150, null=True, verbose_name='Immediate supervisor')),
                ('supervisor_position', models.CharField(blank=True, max_length=150, null=True, verbose_name='Position of immediate supervisor')),
                ('reasons_for_leave', models.TextField(blank=True, null=True)),
                ('application', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='employments', to='application.application')),
            ],
        ),
        migrations.CreateModel(
            name='OtherReferences',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Reference Name')),
                ('address', models.CharField(blank=True, max_length=50, null=True, verbose_name='Reference Address')),
                ('company', models.CharField(blank=True, max_length=50, null=True, verbose_name='Reference Company')),
                ('position', models.CharField(blank=True, max_length=50, null=True, verbose_name='Reference Position')),
                ('reference_phone_number', models.CharField(blank=True, max_length=11, null=True)),
                ('application', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='other_references', to='application.application')),
            ],
            options={
                'verbose_name_plural': 'Other References',
            },
        ),
        migrations.CreateModel(
            name='JobQualification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qualification', models.CharField(max_length=300)),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='qualifications', to='application.job')),
            ],
        ),
        migrations.CreateModel(
            name='JobDescription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=300)),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='job_descriptions', to='application.job')),
            ],
        ),
        migrations.AddField(
            model_name='job',
            name='section',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='application.jobsection'),
        ),
        migrations.CreateModel(
            name='Apply',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('issue_date', models.DateTimeField(auto_created=True, db_index=True)),
                ('full_name', models.CharField(max_length=250)),
                ('mobile', models.CharField(max_length=12)),
                ('email_address', models.EmailField(max_length=254)),
                ('message', models.TextField(blank=True, null=True)),
                ('resume', models.FileField(blank=True, null=True, upload_to='resume', validators=[employee.validators.validate_file_extension])),
                ('status', models.CharField(choices=[('C', 'Yes, I am a current employee'), ('F', 'Yes, I am a former employee'), ('N', 'No')], default='N', help_text='Are you a current or former Red Sea 24 company employee?', max_length=1)),
                ('job', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='application.job')),
            ],
            options={
                'verbose_name_plural': 'Applies',
            },
        ),
        migrations.CreateModel(
            name='ApplicationLanguages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('speaking', models.CharField(choices=[('E', 'Excellent'), ('G', 'Good'), ('F', 'Fair')], db_index=True, default='G', max_length=1)),
                ('writing', models.CharField(choices=[('E', 'Excellent'), ('G', 'Good'), ('F', 'Fair')], db_index=True, default='G', max_length=1)),
                ('reading', models.CharField(choices=[('E', 'Excellent'), ('G', 'Good'), ('F', 'Fair')], db_index=True, default='G', max_length=1)),
                ('application', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='languages', to='application.application')),
                ('language', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='application.language')),
            ],
            options={
                'verbose_name_plural': 'Application Languages',
            },
        ),
        migrations.CreateModel(
            name='ApplicationEducation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('school', models.CharField(max_length=50, verbose_name='Name of school')),
                ('degree', models.CharField(max_length=20)),
                ('year', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1984), django.core.validators.MaxValueValidator(2022)])),
                ('application', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='education', to='application.application')),
            ],
        ),
        migrations.AddField(
            model_name='application',
            name='position',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='application.position'),
        ),
    ]