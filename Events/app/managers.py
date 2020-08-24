from django.db import models
from django.contrib.auth.models import User

class PatientManager(models.Manager):
    def by_user(self, user):
        return self.filter(author__user=user, is_active=True)

    def newest(self, user):
        return self.by_user(user).order_by('-pk')
    
    def starts_with(self, pattern, user):
        return self.by_user(user).filter(name__istartswith=pattern)
    
    def contains(self, pattern, user):
        return self.by_user(user).filter(name__icontains=pattern)
    
    def delete(self, pid):
        from app.models import Event
        patient = self.get(pk=pid)
        Event.objects.delete_by_patient(pid)
        patient.is_active = False
        patient.save()

class EventManager(models.Manager):
    def by_user(self, user):
        return self.filter(author__user=user, is_active=True)

    def newest(self, user):
        return self.by_user(user).order_by('-pk')

    def by_day(self, day, user):
        return self.by_user(user).filter(date__day=day)

    def by_date(self, date, user):
        return self.by_user(user).filter(date=date)
    
    def by_patient(self, pid, user):
        return self.by_user(user).filter(patient__id=pid).order_by('-date')
    
    def by_procedure(self, pid, user):
        return self.by_user(user).filter(procedures__id=pid).order_by('-date')
    
    def delete(self, eid):
        event = self.get(pk=eid)
        event.is_active = False
        event.save()
    
    def delete_by_patient(self, pid):
        events = self.by_user(user).filter(patient__id=pid)
        for event in events:
            event.is_active = False
            event.save()
    
    def medication_list(self, pattern, user):
        events = self.by_user(user).filter(medication__istartswith=pattern)
        medications = list()
        for event in events:
            medications.append(event.medication)
        return medications

class ProcedureManager(models.Manager):
    def by_user(self, user):
        return self.filter(author__user=user, is_active=True)

    def newest(self, user):
        return self.by_user(user).order_by('-pk')
    
    def delete(self, pid):
        procedure = self.get(pk=pid)
        procedure.is_active = False
        procedure.save()

class ProfileManager(models.Manager):
    def is_username_exists(self, username):
        return User.objects.filter(username=username).exists()
    
    def is_email_exists(self, email):
        return User.objects.filter(email=email).exists()
    
    def by_user(self, user):
        return self.get(user=user)
