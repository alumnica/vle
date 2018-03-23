from datetime import date
from django import forms

from alumnica_model.models import LearnerModel


class FirstLoginInfoForm(forms.ModelForm):
    first_name = forms.CharField()
    last_name = forms.CharField()
    gender_field = forms.CharField(widget=forms.RadioSelect(attrs= {'display':'inline-block'},
                                                            choices=LearnerModel.GENDER_TYPES))
    birth_date_field = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = LearnerModel
        fields = ['birth_date_field', 'gender_field']

    def save_form(self, user):
        cleaned_data = super(FirstLoginInfoForm, self).clean()
        user.first_name = cleaned_data.get('first_name')
        user.last_name = cleaned_data.get('last_name')
        profile = user.profile
        profile.birth_date = date.today().__str__()
        user.save()