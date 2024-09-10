# Generated by Django 5.1.1 on 2024-09-10 10:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('brreg_api', '0003_alter_company_forretningsadresse_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='PageResult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('page_number', models.IntegerField(unique=True)),
                ('as_count', models.IntegerField(default=0)),
                ('bankrupt_count', models.IntegerField(default=0)),
            ],
        ),
    ]