from django.db import models

class PatientManager(models.Manager):
    def newest(self):
        return self.filter(is_active=True).order_by('-pk')
    
    def starts_with(self, pattern):
        return self.newest().filter(name__istartswith=pattern)
    
    def contains(self, pattern):
        return self.newest().filter(name__icontains=pattern)
    
    def delete(self, pid):
        from app.models import Event
        patient = self.get(pk=pid)
        Event.objects.delete_by_patient(pid)
        patient.is_active = False
        patient.save()

class EventManager(models.Manager):
    def newest(self):
        return self.filter(is_active=True).order_by('-pk')

    def by_day(self, day):
        return self.filter(is_active=True).filter(date__day=day)

    def by_date(self, date):
        return self.filter(is_active=True).filter(date=date)
    
    def medication_list(self, pattern):
        events = self.filter(is_active=True).filter(medication__istartswith=pattern)
        medications = list()
        for event in events:
            medications.append(event.medication)
        return medications
    
    def by_patient(self, pid):
        return self.filter(is_active=True).filter(patient__id=pid).order_by('-date')
    
    def by_procedure(self, pid):
        return self.filter(is_active=True).filter(procedures__id=pid).order_by('-date')
    
    def delete(self, eid):
        event = self.get(pk=eid)
        event.is_active = False
        event.save()
    
    def delete_by_patient(self, pid):
        events = self.filter(is_active=True).filter(patient__id=pid)
        for event in events:
            event.is_active = False
            event.save()

class ProcedureManager(models.Manager):
    def newest(self):
        return self.filter(is_active=True).order_by('-pk')
    
    def delete(self, pid):
        procedure = self.get(pk=pid)
        procedure.is_active = False
        procedure.save()

class ProfileManager(models.Manager):
    def is_exist(self, username):
        return User.objects.filter(username=username).exists()
