# Generated by Django 4.0.1 on 2022-04-27 18:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='jobqualification',
            name='job',
        ),
        migrations.AlterModelOptions(
            name='apply',
            options={'ordering': ('-issue_date',), 'verbose_name_plural': 'Apply Requests'},
        ),
        migrations.AlterModelOptions(
            name='job',
            options={'ordering': ('post_date',)},
        ),
        migrations.AddField(
            model_name='job',
            name='job_description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='job',
            name='qualifications',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.DeleteModel(
            name='JobDescription',
        ),
        migrations.DeleteModel(
            name='JobQualification',
        ),
    ]
