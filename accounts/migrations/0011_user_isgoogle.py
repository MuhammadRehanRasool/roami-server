# Generated by Django 4.2.1 on 2023-08-13 16:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0010_profile_list_import_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='isGoogle',
            field=models.BooleanField(default=False),
        ),
    ]