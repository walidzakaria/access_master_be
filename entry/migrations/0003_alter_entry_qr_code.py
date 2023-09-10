# Generated by Django 4.0.1 on 2023-09-10 22:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('entry', '0002_alter_entry_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entry',
            name='qr_code',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='entry.qrcode', unique=True),
        ),
    ]