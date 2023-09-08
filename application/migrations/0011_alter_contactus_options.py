
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0010_contactus'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='contactus',
            options={'ordering': ('-date',), 'verbose_name_plural': 'Contact us'},
        ),
    ]
