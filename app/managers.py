from django.db import models

class PatientManager(models.Manager):
    def newest(self):
        return self.filter(is_active=True).order_by('-pub_date')

class EventManager(models.Manager):
    def by_date(self, d):
        return self.filter(date=d)

class ProcedureManager(models.Manager):
    pass
