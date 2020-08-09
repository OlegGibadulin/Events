from django.db import models

class PatientManager(models.Manager):
    def newest(self):
        return self.order_by('-pk')

class EventManager(models.Manager):
    def by_date(self, d):
        return self.filter(date=d)

class ProcedureManager(models.Manager):
    def newest(self):
        return self.order_by('-pk')

class ProfileManager(models.Manager):
    def is_exist(self, name, email):
        return User.objects.filter(username=name).count()
