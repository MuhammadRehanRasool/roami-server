# Generated by Django 4.2.1 on 2023-08-17 21:40

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PopularLists',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.IntegerField(unique=True)),
            ],
            options={
                'verbose_name': 'Popular List',
                'verbose_name_plural': 'Popular Lists',
            },
        ),
        migrations.CreateModel(
            name='Sections',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('heading', models.CharField(max_length=256)),
                ('content', models.TextField(blank=True, null=True)),
                ('call', models.CharField(help_text='Text for button.', max_length=256)),
                ('url', models.URLField(blank=True, help_text='URL for button.', null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='about_images')),
                ('order', models.IntegerField(unique=True)),
                ('alignRight', models.BooleanField(default=True, help_text='Display image on right side?')),
            ],
            options={
                'verbose_name': 'Section',
                'verbose_name_plural': 'Sections',
            },
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
                ('content', models.TextField(blank=True, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='about_team_images')),
                ('order', models.IntegerField(unique=True)),
            ],
            options={
                'verbose_name': 'Team',
                'verbose_name_plural': 'Teams',
            },
        ),
    ]
