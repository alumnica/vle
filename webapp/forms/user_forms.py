from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from alumnica_model.models import AuthUser


class UserForm(forms.ModelForm):
<<<<<<< HEAD
    password1 = forms.CharField(widget=forms.PasswordInput())
    password2 = forms.CharField(widget=forms.PasswordInput())
    user_type = forms.CharField()
=======
    password = forms.CharField(widget=forms.PasswordInput())
    password_confirmation = forms.CharField(widget=forms.PasswordInput())

>>>>>>> da9c0a46540845372681e37725917f818122afbf
    class Meta:
        model = AuthUser
        fields = ['email', 'password', 'password_confirmation']

<<<<<<< HEAD
    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['user_type'].initial = UserType.LEARNER
=======
    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        password = cleaned_data.get('password')
        password_confirmation = cleaned_data.get('password_confirmation')
>>>>>>> da9c0a46540845372681e37725917f818122afbf

        if password != password_confirmation:
            error = ValidationError(_("The two password fields didn't match."), code='password_mismatch')
            self.add_error('password', error)
            self.add_error('password_confirmation', error)

<<<<<<< HEAD
class LearnerForm(forms.ModelForm):
    class Meta:
        model = LearnerModel
        exclude = ['auth_user_field']

class UserLoginForm(forms.ModelForm):
    pass
=======
        return cleaned_data

    def save(self, commit=True):
        user = super(UserForm, self).save(commit)
        user.set_password(self.cleaned_data.get('password'))

        if commit:
            user.save()

        return user
>>>>>>> da9c0a46540845372681e37725917f818122afbf
