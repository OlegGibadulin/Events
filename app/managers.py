from django.db import models

class PatientManager(models.Manager):
    def newest(self):
        return self.order_by('-pk')
    
    def starts_with(self, pattern):
        return self.filter(name__istartswith=pattern)
    
    def contains(self, pattern):
        return self.filter(name__icontains=pattern)

class EventManager(models.Manager):
    def by_date(self, d):
        return self.filter(date=d)
    
    def medication_list(self, pattern):
        events = self.filter(medication__istartswith=pattern)
        medications = list()
        for event in events:
            medications.append(event.medication)
        return medications

class ProcedureManager(models.Manager):
    def newest(self):
        return self.order_by('-pk')

class ProfileManager(models.Manager):
    def is_exist(self, name, email):
        return User.objects.filter(username=name).count()
