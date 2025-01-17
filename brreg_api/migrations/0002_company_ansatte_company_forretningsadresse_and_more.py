# Generated by Django 5.1.1 on 2024-09-10 08:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('brreg_api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='ansatte',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='company',
            name='forretningsadresse',
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='company',
            name='frivilligMvaRegistrertBeskrivelser',
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='company',
            name='naeringskode1',
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='company',
            name='org_form',
            field=models.CharField(default='', max_length=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='company',
            name='postadresse',
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='company',
            name='registreringsdatoEnhetsregisteret',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='company',
            name='registrertIMvaregisteret',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='company',
            name='stiftelsesdato',
            field=models.DateField(blank=True, null=True),
        ),
    ]
