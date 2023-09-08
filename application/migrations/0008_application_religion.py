# Generated by Django 4.0.1 on 2022-05-29 11:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0007_alter_application_mother_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='application',
            name='religion',
            field=models.CharField(choices=[('M', 'Muslim'), ('C', 'Christian'), ('O', 'Other')], default='M', max_length=1),
        ),
    ]