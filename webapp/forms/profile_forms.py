from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from alumnica_model.models import Learner, users, AuthUser
from alumnica_model.models.content import LearningStyle
from alumnica_model.models.progress import EXPERIENCE_POINTS_CONSTANTS


class FirstLoginInfoForm(forms.ModelForm):
    first_name = forms.CharField()
    last_name = forms.CharField()
    gender_field = forms.CharField(widget=forms.RadioSelect(attrs={'display': 'inline'}, choices=users.GENDER_TYPES))
    birth_date_field = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Learner
        fields = ['birth_date_field', 'gender_field']

    def save_form(self, user):
        cleaned_data = super(FirstLoginInfoForm, self).clean()
        user.first_name = cleaned_data.get('first_name')
        user.last_name = cleaned_data.get('last_name')
        profile = user.profile
        profile.birth_date = cleaned_data.get('birth_date_field')
        profile.gender = cleaned_data.get('gender_field')
        user.save()


class FirstLoginP1(forms.Form):
    pass


class FirstLoginP2(forms.Form):
    def save_form(self, user, first_selection, second_selection):
        option_1 = first_selection
        option_2 = second_selection
        profile = user.profile

        if profile.learning_style is None:
            profile.experience_points += EXPERIENCE_POINTS_CONSTANTS['learning_short_quiz']

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


class FirstLoginP3(forms.Form):
    def save_form(self, user, first_selection, second_selection):
        option_1 = first_selection
        option_2 = second_selection
        profile = user.profile

        if profile.learning_style is None:
            profile.experience_points += EXPERIENCE_POINTS_CONSTANTS['learning_short_quiz']

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
    gender_field = forms.CharField(widget=forms.RadioSelect(attrs={'display': 'inline'}, choices=users.GENDER_TYPES))
    birth_date_field = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    previous_password = forms.CharField(required=False, widget=forms.PasswordInput())
    new_password = forms.CharField(required=False, widget=forms.PasswordInput())
    new_password_confirmation = forms.CharField(required=False, widget=forms.PasswordInput())


    class Meta:
        model = AuthUser
        fields = ['first_name', 'last_name']

    def __init__(self, *args, **kwargs):
        super(ProfileSettingsForm, self).__init__(*args, **kwargs)
        user = AuthUser.objects.get(pk=kwargs['instance'].pk)
        self.fields['gender_field'].initial = user.profile.gender
        self.fields['birth_date_field'].initial = user.profile.birth_date

    def clean(self):
        cleaned_data = super(ProfileSettingsForm, self).clean()

        previous_password = cleaned_data.get('previous_password')
        new_password = cleaned_data.get('new_password')
        new_password_confirmation = cleaned_data.get('new_password_confirmation')

        if previous_password is not '' or new_password is not '' or new_password_confirmation is not '':
            if new_password is '':
                error = ValidationError(_("Write a new password"), code='password_error')
                self.add_error('new_password', error)
            else:
                if len(new_password) < 6:
                    error = ValidationError(_("Password must have 6 characters or more."), code='password_length_error')
                    self.add_error('new_password', error)
                else:
                    if new_password_confirmation is '':
                        error = ValidationError(_("Please write the password confirmation."),
                                                code='password_confirmation_error')
                        self.add_error('new_password_confirmation', error)
                    else:
                        if new_password != new_password_confirmation:
                            error = ValidationError(_("Passwords do not match."),
                                                    code='password_confirmation_error')
                            self.add_error('new_password', error)
                        else:
                            if previous_password is not '':
                                user = self.instance
                                if not user.check_password(previous_password):
                                    error = ValidationError(_("Invalid password."), code='credentials_error')
                                    self.add_error('previous_password', error)
                            else:
                                error = ValidationError(_("Previous password must be written."), code='credentials_error')
                                self.add_error('previous_password', error)

        return cleaned_data

    def save(self, commit=True):
        user = super(ProfileSettingsForm, self).save(commit=False)
        new_password = self.cleaned_data.get('new_password')
        if new_password != '':
            user.set_password(self.cleaned_data.get('new_password'))
        user.save()
        return user

