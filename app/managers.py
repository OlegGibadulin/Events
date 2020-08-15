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
    
    def by_patient(self, pid):
        return self.filter(patient__id=pid).order_by('-date')
    
    def by_procedure(self, procedure_title):
        return self.filter(procedures__title=procedure_title).order_by('-date')

class ProcedureManager(models.Manager):
    def newest(self):
        return self.order_by('-pk')

class ProfileManager(models.Manager):
    def is_exist(self, name, email):
        return User.objects.filter(username=name).count()
