# Generated by Django 4.0.1 on 2022-12-11 15:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0012_applicationstatus'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='applicationstatus',
            options={'verbose_name_plural': 'Application Status'},
        ),
        migrations.AlterField(
            model_name='applicationstatus',
            name='issue_date',
            field=models.DateTimeField(auto_now=True),
        ),
    ]