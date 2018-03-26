
from django import forms
from django.utils.safestring import mark_safe

from alumnica_model.models import LearnerModel
from alumnica_model.models.content import LearningStyleModel

P1CHOICES = (
  (1, mark_safe('<img src="http://via.placeholder.com/200x300" alt="approve" title="approve">')),
  (2, mark_safe('<img src="http://via.placeholder.com/200x300" alt="disapprove" title="disapprove">')),
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


class FirstLoginP22(forms.Form):
    learning_options = forms.CharField(widget=forms.RadioSelect(choices=P22CHOICES))


    def save_form(self, user, first_selection):
        cleaned_data = super(FirstLoginP22, self).clean()
        option_1 = first_selection
        option_2 = cleaned_data.get('learning_options')
        profile = user.profile

        if option_1 == '1':
            if option_2 == '1':
                profile.learning_style = LearningStyleModel.objects.get(name_field='Acomodador')
            else:
                profile.learning_style = LearningStyleModel.objects.get(name_field='Divergente')
        elif option_1 == '2':
            if option_2 == '1':
                profile.learning_style = LearningStyleModel.objects.get(name_field='Convergente')
            else:
                profile.learning_style = LearningStyleModel.objects.get(name_field='Asimilador')

        user.save()



class FirstLoginP31(forms.Form):
    learning_options = forms.CharField(widget=forms.RadioSelect(choices=P31CHOICES))


class FirstLoginP32(forms.Form):
    learning_options = forms.CharField(widget=forms.RadioSelect(choices=P32CHOICES))

    def save_form(self, user, first_selection):
        cleaned_data = super(FirstLoginP32, self).clean()
        option_1 = first_selection
        option_2 = cleaned_data.get('learning_options')
        profile = user.profile

        if option_1 == '1':
            if option_2 == '1':
                profile.learning_style = LearningStyleModel.objects.get(name_field='Convergente')
            else:
                profile.learning_style = LearningStyleModel.objects.get(name_field='Asimilador')
        elif option_1 == '2':
            if option_2 == '1':
                profile.learning_style = LearningStyleModel.objects.get(name_field='Acomodador')
            else:
                profile.learning_style = LearningStyleModel.objects.get(name_field='Divergente')

        user.save()
