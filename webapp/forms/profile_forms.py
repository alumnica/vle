
from django import forms
from django.utils.safestring import mark_safe

from alumnica_model.models import LearnerModel

P1CHOICES = (
  (2, mark_safe('<img src="http://via.placeholder.com/200x300" alt="approve" title="approve">')),
  (3, mark_safe('<img src="http://via.placeholder.com/200x300" alt="disapprove" title="disapprove">')),
)

P21CHOICES = (
  (1, mark_safe('<img src="http://via.placeholder.com/200x300" alt="approve" title="approve">')),
  (2, mark_safe('<img src="http://via.placeholder.com/200x300" alt="disapprove" title="disapprove">')),
)

P22CHOICES = (
  (1, mark_safe('<img src="http://via.placeholder.com/200x300" alt="approve" title="approve">')),
  (2, mark_safe('<img src="http://via.placeholder.com/200x300" alt="disapprove" title="disapprove">')),
)

P31CHOICES = (
  (1, mark_safe('<img src="http://via.placeholder.com/200x300" alt="approve" title="approve">')),
  (2, mark_safe('<img src="http://via.placeholder.com/200x300" alt="disapprove" title="disapprove">')),
)

P32CHOICES = (
  (1, mark_safe('<img src="http://via.placeholder.com/200x300" alt="approve" title="approve">')),
  (2, mark_safe('<img src="http://via.placeholder.com/200x300" alt="disapprove" title="disapprove">')),
)


class FirstLoginInfoForm(forms.ModelForm):
    first_name = forms.CharField()
    last_name = forms.CharField()
    gender_field = forms.CharField(widget=forms.RadioSelect(attrs={'display':'inline'},
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
        profile.birth_date = cleaned_data.get('birth_date_field')
        profile.gender = cleaned_data.get('gender_field')
        user.save()


class FirstLoginP1(forms.Form):
    learning_options = forms.CharField(widget=forms.RadioSelect(choices=P1CHOICES))


class FirstLoginP21(forms.Form):
    learning_options = forms.CharField(widget=forms.RadioSelect(choices=P21CHOICES))


