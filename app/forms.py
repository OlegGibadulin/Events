from django.forms import ModelForm, DateInput, TextInput, CharField
from app.models import Event, Patient, Procedure

class EventForm(ModelForm):
    # temp_id = CharField(label = 'extra_field', required = False)

    class Meta:
        model = Event
        exclude = ['price']

        # widgets = {
        #     'date': DateInput(attrs={'type': 'date'}, format='%Y-%m-%dT'),
        #     'procedures': TextInput(attrs={'size': '20'}),
        #     'patient': TextInput(attrs={'size': '20'}),
        # }

        widgets = {
            'date': DateInput(attrs={'type': 'date'}),
        }

        labels = {
            'date': 'Дата',
            'procedures': 'Процедуры',
            'patient': 'Пациент',
        }

    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)

class PatientForm(ModelForm):
    class Meta:
        model = Patient
        # fields = ['name', 'description']
        exclude = ['is_active', 'pub_date']

class ProcedureForm(ModelForm):
    class Meta:
        model = Procedure
        exclude = ['ref_num']
