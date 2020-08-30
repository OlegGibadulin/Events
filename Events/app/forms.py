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
                'placeholder': 'Введите название препарата', 'id': 'medication'}),
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
                'placeholder': 'Введите имя пациента', 'id': '',
                'autofocus': 'autofocus'}),
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
                'placeholder': 'Введите название процедуры',
                'id': '', 'autofocus': 'autofocus'}),
        }

        labels = {
            'title': 'Название процедуры'
        }
    
    def __init__(self, *args, **kwargs):
        super(ProcedureForm, self).__init__(*args, **kwargs)
        self.label_suffix=''


from app.models import UserProfile

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
import django.contrib.auth as auth

class RegisterForm(forms.ModelForm):
    error_messages = {
        'password_mismatch': 'Пароли не совпадают',
        'username_already_exists': 'Данный логин уже используется',
        'email_already_exists': 'Данный Email уже используется',
    }

    username = forms.CharField(
        label=('Логин'),
        widget=forms.TextInput(attrs={'class': 'form-control',
            'placeholder': 'Введите логин', 'id': 'id_username',
            'autofocus': 'autofocus'}),
    )

    email = forms.EmailField(
        label=('Email'),
        widget=forms.EmailInput(attrs={'class': 'form-control',
            'placeholder': 'Введите Email'}),
    )

    password1 = forms.CharField(
        label=('Пароль'),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password',
            'class': 'form-control', 'placeholder': 'Введите пароль'}),
    )

    password2 = forms.CharField(
        label=('Подтверждение пароля'),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password',
            'class': 'form-control', 'placeholder': 'Повторите пароль'}),
    )

    class Meta:
        model = UserProfile
        fields = []
    
    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.label_suffix=''
    
    def clean_username(self):
        username = self.cleaned_data['username']
        if UserProfile.objects.is_username_exists(username):
            raise forms.ValidationError(
                self.error_messages['username_already_exists'],
                code='username_already_exists',
            )
        return username
    
    def clean_email(self):
        email = self.cleaned_data['email']
        if UserProfile.objects.is_email_exists(email):
            raise forms.ValidationError(
                self.error_messages['email_already_exists'],
                code='email_already_exists',
            )
        return email
    
    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2
    
    def save(self):
        username = self.cleaned_data['username']
        email = self.cleaned_data['email']
        password = self.cleaned_data['password1']
        self.user_cache = User.objects.create_user(
            username=username, email=email, password=password
        )
        UserProfile.objects.create(user=self.user_cache)
    
    def get_user(self):
        return self.user_cache

class LoginForm(forms.ModelForm):
    error_messages = {
        'invalid_login': 'Неправильный Email или пароль',
        'inactive': 'Этот аккаунт удалён',
    }

    username = forms.CharField(
        label=('Логин'),
        widget=forms.TextInput(attrs={'class': 'form-control',
            'placeholder': 'Введите логин', 'id': '',
            'autofocus': 'autofocus'}),
    )

    password = forms.CharField(
        label=('Пароль'),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password',
            'class': 'form-control', 'placeholder': 'Введите пароль'}),
    )

    class Meta:
        model = UserProfile
        fields = []
    
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.label_suffix=''
    
    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            self.user_cache = auth.authenticate(username=username,
                                           password=password)
            if self.user_cache is None:
                raise forms.ValidationError(
                    self.error_messages['invalid_login'],
                    code='invalid_login',
                )
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data
    
    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise forms.ValidationError(
                self.error_messages['inactive'],
                code='inactive',
            )
    
    def get_user(self):
        return self.user_cache
