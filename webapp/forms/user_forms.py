from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from alumnica_model.models import AuthUser


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    password_confirmation = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = AuthUser
        fields = ['email', 'password', 'password_confirmation']

    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        password = cleaned_data.get('password')
        password_confirmation = cleaned_data.get('password_confirmation')

        if password != password_confirmation:
            error = ValidationError(_("The two password fields didn't match."), code='password_mismatch')
            self.add_error('password', error)
            self.add_error('password_confirmation', error)
        return cleaned_data

    def save(self, commit=True):
        user = super(UserForm, self).save(commit)
        user.set_password(self.cleaned_data.get('password'))

        if commit:
            user.save()

        return user


class UserLoginForm(forms.Form):
    email = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput())

    def clean(self):
        cleaned_data = super(UserLoginForm, self).clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')
        try:
            user = AuthUser.objects.get(email=email)
            if not user.check_password(password):
                error = ValidationError(_("Invalid password or email."), code='password_mismatch')
                self.add_error('password', error)
                self.add_error('email', error)

        except AuthUser.DoesNotExist:
            error = ValidationError(_("Invalid password or email."), code='password_mismatch')
            self.add_error('password', error)
            self.add_error('email', error)
        return cleaned_data

    def get_user(self):
        cleaned_data = super(UserLoginForm, self).clean()
        email = cleaned_data.get('email')
        user = AuthUser.objects.get(email=email)
        return user
