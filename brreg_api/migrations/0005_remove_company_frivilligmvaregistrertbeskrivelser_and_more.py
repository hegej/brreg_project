# Generated by Django 5.1.1 on 2024-09-10 11:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('brreg_api', '0004_pageresult'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='company',
            name='frivilligMvaRegistrertBeskrivelser',
        ),
        migrations.RemoveField(
            model_name='company',
            name='is_as',
        ),
    ]