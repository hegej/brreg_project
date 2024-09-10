from django.db import models


class Company(models.Model):
    org_number = models.CharField(max_length=9, unique=True)
    name = models.CharField(max_length=255)
    org_form = models.CharField(max_length=10, default='')
    is_bankrupt = models.BooleanField(default=False)
    is_as = models.BooleanField(default=False)
    postadresse = models.JSONField(null=True, blank=True, default=dict)
    forretningsadresse = models.JSONField(null=True, blank=True, default=dict)
    naeringskode1 = models.JSONField(null=True, blank=True, default=dict)
    ansatte = models.IntegerField(null=True, blank=True)
    stiftelsesdato = models.DateField(null=True, blank=True)
    registreringsdatoEnhetsregisteret = models.DateField(null=True, blank=True)
    registrertIMvaregisteret = models.BooleanField(default=False)
    frivilligMvaRegistrertBeskrivelser = models.JSONField(null=True, blank=True, default=list)
    updated_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.org_number})"