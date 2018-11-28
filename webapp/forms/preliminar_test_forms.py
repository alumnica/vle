from django import forms
from rest_framework.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from alumnica_model.models import AuthUser, Learner, users
from alumnica_model.validators import validate_date


class TestUserLoginForm(forms.Form):
    """
    Login form
    """
    email = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput())

    def clean(self):
        cleaned_data = super(TestUserLoginForm, self).clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')
        try:
            user = AuthUser.objects.get(email=email)
            if not user.check_password(password):
                error = ValidationError(_("Contraseña o correo incorrecto"), code='credentials_error')
                self.add_error('password', error)
                return cleaned_data

        except AuthUser.DoesNotExist:
            error = ValidationError(_("Contraseña o correo incorrecto"), code='credentials_error')
            self.add_error('password', error)
            return cleaned_data

    def get_user(self):
        cleaned_data = super(TestUserLoginForm, self).clean()
        email = cleaned_data.get('email')
        user = AuthUser.objects.get(email=email)
        return user


class FirstLoginTestInfoForm(forms.ModelForm):
    """
    Personal information form
    """
    first_name = forms.CharField()
    last_name = forms.CharField()
    birth_date_field = forms.DateField(validators=[validate_date], widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Learner
        fields = ['birth_date_field']

    def save_form(self, user, gender):
        cleaned_data = super(FirstLoginTestInfoForm, self).clean()
        user.first_name = cleaned_data.get('first_name')
        user.last_name = cleaned_data.get('last_name')
        profile = user.profile
        profile.birth_date = cleaned_data.get('birth_date_field')
        profile.gender = gender
        user.save()


class FirstLoginTest(forms.Form):
    """
    Short learning style quiz
    """

    def save_form(self, user, first_selection, second_selection):
        pass
