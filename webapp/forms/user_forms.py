import csv

from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.password_validation import MinimumLengthValidator, CommonPasswordValidator, \
    NumericPasswordValidator, validate_password
from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.utils.encoding import smart_str
from django.utils.translation import gettext_lazy as _

from alumnica_model.models import AuthUser, Learner


class UserForm(forms.ModelForm):
    """
    Create new AuthUser form
    """
    password = forms.CharField(widget=forms.PasswordInput())
    password_confirmation = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = AuthUser
        fields = ['email', 'password', 'password_confirmation']

    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        user = super(UserForm, self).save(commit=False)
        password = cleaned_data.get('password')
        password_confirmation = cleaned_data.get('password_confirmation')

        try:
            validate_password(password, user)
            if password != password_confirmation:
                error = ValidationError(_("Las contraseñas no coinciden"), code='password_mismatch')
                self.add_error('password', error)
                self.add_error('password_confirmation', error)
        except ValidationError as error:
            if error.error_list[0].code == 'password_too_common':
                error = ValidationError('La contraseña es muy común',
                                        code='password_error')
            elif error.error_list[0].code == 'password_entirely_numeric':
                error = ValidationError('La contraseña no debe contener sólo números',
                                        code='password_error')
            elif error.error_list[0].code == 'password_too_short':
                error = ValidationError('La contraseña debe contener al menos {} caracteres'.format(error.error_list[0].params['min_length']),
                                        code='password_error')
            self.add_error('password', error)

        return cleaned_data

    def save(self, commit=True):
        user = super(UserForm, self).save(commit)
        user.set_password(self.cleaned_data.get('password'))

        if commit:
            user.save()

        return user


class UserLoginForm(forms.Form):
    """
    Login form
    """
    email = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput())

    def clean(self):
        cleaned_data = super(UserLoginForm, self).clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')
        try:
            user = AuthUser.objects.get(email=email)
            if not user.check_password(password):
                error = ValidationError(_("Contraseña o correo incorrecto"), code='credentials_error')
                self.add_error('password', error)
                return cleaned_data
            if not user.is_active:
                error = ValidationError(_("Tu cuenta no ha sido activada"), code='account_activation_error')
                self.add_error('email', error)
                return cleaned_data

        except AuthUser.DoesNotExist:
            error = ValidationError(_("Contraseña o correo incorrecto"), code='credentials_error')
            self.add_error('password', error)
            return cleaned_data

    def get_user(self):
        cleaned_data = super(UserLoginForm, self).clean()
        email = cleaned_data.get('email')
        user = AuthUser.objects.get(email=email)
        return user


class AuthUserCreateForm(forms.ModelForm):
    """
    Create new AuthUser form for Django Administration
    """

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
    """
    Adds files to AuthUserCreateForm form
    """
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


def download_learner_file(modeladmin, request, queryset):
    """
    Downloads CSV file containing Learner profiles selected in Django Administration page by selecting Export CSV
    :param queryset: Selected Learner objects
    :return: CSV file
    """
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
            smart_str('{} {}'.format(obj.auth_user.first_name, obj.auth_user.last_name)),
            smart_str(obj.auth_user.email),
            smart_str(obj.birth_date),
            smart_str(obj.learning_style),
        ])
    return response


download_learner_file.short_description = u"Export CSV"


class DownloadLearnerFile(admin.ModelAdmin):
    """
    Displays the action in the Learner model page
    """
    actions = [download_learner_file]


admin.site.unregister(AuthUser)
admin.site.unregister(Learner)
admin.site.register(Learner, DownloadLearnerFile)
admin.site.register(AuthUser, CustomUserAdmin)
