from django import forms

from alumnica_model.alumnica_entities.users import UserType
from alumnica_model.models import LearnerModel, AuthUser


class UserForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput())
    password2 = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = AuthUser
        fields = ['username', 'email', 'password1', 'password2', 'user_type']

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['user_type'] = UserType.LEARNER


class LearnerForm(forms.ModelForm):
    class Meta:
        model = LearnerModel
        exclude = ['auth_user_field']