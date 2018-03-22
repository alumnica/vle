from django import forms


class FirstLoginInfoForm(forms.Form):
    fisrt_name = forms.CharField()
    last_name = forms.CharField()
    birthday = forms.DateField(widget=forms.DateInput)
    gender = forms.CharField()