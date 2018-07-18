from django import forms

from alumnica_model.models import Learner, users, AuthUser
from alumnica_model.models.content import LearningStyle


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
            profile.experience_points += 1000

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
            profile.experience_points += 1000

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
    password = forms.CharField(widget=forms.PasswordInput())
    gender_field = forms.CharField(widget=forms.RadioSelect(attrs={'display': 'inline'}, choices=users.GENDER_TYPES))
    birth_date_field = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = AuthUser
        fields = ['email', 'password', 'first_name', 'last_name']
