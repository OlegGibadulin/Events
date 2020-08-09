from django import forms
from app.models import Event, Patient, Procedure

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['date', 'patient', 'procedures', 'medication', 'body_area', 'notes']

        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'patient': forms.Select(attrs={'class': 'form-control'}),
            'procedures': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'medication': forms.TextInput(attrs={'class': 'form-control',
                'placeholder': 'Введите название препарата'}),
            'body_area': forms.TextInput(attrs={'class': 'form-control', 
                'placeholder': 'Введите область применения'}),
            'notes': forms.Textarea(attrs={'class': 'form-control',
                'placeholder': 'Оставьте заметки'}),
        }

        labels = {
            'date': 'Дата',
            'patient': 'Пациент',
            'procedures': 'Процедура',
            'medication': 'Препарат',
            'body_area': 'Область',
            'notes': 'Заметки',
        }

    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        self.label_suffix=''

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['name', 'description']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control',
                'placeholder': 'Введите имя пациента'}),
            'description': forms.Textarea(attrs={'class': 'form-control',
                'placeholder': 'Заполните карту пациента'}),
        }

        labels = {
            'name': 'Имя',
            'description': 'Карта пациента',
        }

    def __init__(self, *args, **kwargs):
        super(PatientForm, self).__init__(*args, **kwargs)
        self.label_suffix=''

class ProcedureForm(forms.ModelForm):
    class Meta:
        model = Procedure
        fields = ['title']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control',
                'placeholder': 'Введите название процедуры'}),
        }

        labels = {
            'title': 'Название процедуры'
        }
    
    def __init__(self, *args, **kwargs):
        super(ProcedureForm, self).__init__(*args, **kwargs)
        self.label_suffix=''
