import csv

from django import forms
from django.contrib.auth.admin import UserAdmin
from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.utils.encoding import smart_str
from django.utils.translation import gettext_lazy as _
from alumnica_model.models import AuthUser, Learner
from django.contrib import admin


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

        if len(password) < 6:
            error = ValidationError(_("Password must have 6 characters or more."), code='password_length_error')
            self.add_error('password', error)
        else:
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
                error = ValidationError(_("Invalid password or email."), code='credentials_error')
                self.add_error('password', error)
                self.add_error('email', error)

        except AuthUser.DoesNotExist:
            error = ValidationError(_("Invalid password or email."), code='credentials_error')
            self.add_error('password', error)
            self.add_error('email', error)
        return cleaned_data

    def get_user(self):
        cleaned_data = super(UserLoginForm, self).clean()
        email = cleaned_data.get('email')
        user = AuthUser.objects.get(email=email)
        return user


class AuthUserCreateForm(forms.ModelForm):
    class Meta:
        model = AuthUser
        fields = ['email']

    def save(self, commit=True):
        user = super(AuthUserCreateForm, self).save(commit=False)
        user.set_password(self.cleaned_data.get('password'))
        if commit:
            user.save()
        return user


class CustomUserAdmin(UserAdmin):
    # The forms to add and change user instances
    add_form = AuthUserCreateForm
    list_display = ("email",)
    ordering = ("email",)

    fieldsets = (
        (None, {'fields': ('email', 'password', 'first_name', 'last_name')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password', 'first_name', 'last_name', 'is_superuser', 'is_staff', 'is_active',
                       'user_type')}
         ),
    )

    filter_horizontal = ()


class LearnersToExport(forms.ModelForm):
    birth_day = forms.DateField()
    learning_style = forms.CharField()

    class Meta:
        model = AuthUser
        fields = ['first_name', 'last_name', 'email']


def DownloadLearnerUsers(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=learners.csv'
    writer = csv.writer(response, csv.excel)
    response.write(u'\ufeff'.encode('utf8'))  # BOM (optional...Excel needs it to open UTF-8 file properly)
    writer.writerow([
        smart_str(u"Name"),
        smart_str(u"Email"),
        smart_str(u"Birthday"),
        smart_str(u"Learning Style"),
    ])
    for obj in queryset:
        writer.writerow([
            smart_str('{} {}'.format(obj.auth_user.first_name,obj.auth_user.last_name)),
            smart_str(obj.auth_user.email),
            smart_str(obj.birth_date),
            smart_str(obj.learning_style),
        ])
    return response


DownloadLearnerUsers.short_description = u"Export CSV"


class DownloadLearnerFile(admin.ModelAdmin):
    actions = [DownloadLearnerUsers]


admin.site.unregister(AuthUser)
admin.site.unregister(Learner)
admin.site.register(Learner, DownloadLearnerFile)
admin.site.register(AuthUser, CustomUserAdmin)