from django.db import models

class Company(models.Model):
    org_number = models.CharField(max_length=9, unique=True)
    name = models.CharField(max_length=255)
    is_bankrupt = models.BooleanField(default=False)
    is_as = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} ({self.org_number})"
