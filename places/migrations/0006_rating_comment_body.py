# Generated by Django 4.2.1 on 2023-06-08 09:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('places', '0005_rating'),
    ]

    operations = [
        migrations.AddField(
            model_name='rating',
            name='comment_body',
            field=models.CharField(default='default', max_length=3000),
            preserve_default=False,
        ),
    ]