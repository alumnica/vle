import datetime

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from alumnica_model.models import Learner, users, AuthUser
from alumnica_model.models.content import LearningStyle
from alumnica_model.validators import validate_date
from webapp.gamification import EXPERIENCE_POINTS_CONSTANTS
from webapp.statement_builders import learning_experience_received, edited_profile


class FirstLoginInfoForm(forms.ModelForm):
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
        cleaned_data = super(FirstLoginInfoForm, self).clean()
        user.first_name = cleaned_data.get('first_name')
        user.last_name = cleaned_data.get('last_name')
        profile = user.profile
        profile.birth_date = cleaned_data.get('birth_date_field')
        profile.gender = gender
        user.save()


class FirstLoginP1(forms.Form):
    """
    Short learning style quiz
    """

    def save_form(self, user, first_selection, second_selection):
        option_1 = first_selection
        option_2 = second_selection
        profile = user.profile

        if option_1 == '1':
            if option_2 == '1':
                profile.learning_style = LearningStyle.objects.get(name='Divergente')
            elif option_2 == '2':
                profile.learning_style = LearningStyle.objects.get(name='Acomodador')
        elif option_1 == '2':
            if option_2 == '1':
                profile.learning_style = LearningStyle.objects.get(name='Asimilador')
            elif option_2 == '2':
                profile.learning_style = LearningStyle.objects.get(name='Convergente')

        user.save()


class ProfileSettingsForm(forms.ModelForm):
    """
    Edit password information form
    """
    password = forms.CharField(required=False, widget=forms.PasswordInput())
    new_password = forms.CharField(required=False, widget=forms.PasswordInput())
    new_password_confirmation = forms.CharField(required=False, widget=forms.PasswordInput())

    class Meta:
        model = AuthUser
        fields = ['password']

    def clean(self):
        cleaned_data = super(ProfileSettingsForm, self).clean()

        password = cleaned_data.get('password')
        new_password = cleaned_data.get('new_password')
        new_password_confirmation = cleaned_data.get('new_password_confirmation')

        if password is not '' or new_password is not '' or new_password_confirmation is not '':
            if new_password is '':
                error = ValidationError(_("Escribe una nueva contraseña"), code='password_error')
                self.add_error('new_password', error)
            else:
                if len(new_password) < 6:
                    error = ValidationError(_("La contraseña debe tener al menos 6 caracteres"),
                                            code='password_length_error')
                    self.add_error('new_password', error)
                else:
                    if new_password_confirmation is '':
                        error = ValidationError(_("Por favor confirma tu contraseña."),
                                                code='password_confirmation_error')
                        self.add_error('new_password_confirmation', error)
                    else:
                        if new_password != new_password_confirmation:
                            error = ValidationError(_("Las contraseñas no coinciden."),
                                                    code='password_confirmation_error')
                            self.add_error('new_password', error)
                        else:
                            if password is not '':
                                user = self.instance
                                if not user.check_password(password):
                                    error = ValidationError(_("Contraseña incorrecta."), code='credentials_error')
                                    self.add_error('password', error)
                            else:
                                error = ValidationError(_("Debes escribir tu contraseña anterior."),
                                                        code='credentials_error')
                                self.add_error('password', error)

        return cleaned_data

    def save(self, commit=True):
        user = super(ProfileSettingsForm, self).save(commit=False)
        cleaned_data = super(ProfileSettingsForm, self).clean()
        new_password = cleaned_data.get('new_password')
        if new_password != '':
            user.set_password(cleaned_data.get('new_password'))
        user.save()
        user.profile.save()
        timestamp = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc).isoformat()
        edited_profile(user=user, timestamp=timestamp)
        return user


class LargeLearningStyleQuizForm(forms.Form):
    """
    Large learning style quiz form
    """

    def save_form(self):
        pass
