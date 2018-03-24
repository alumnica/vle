from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.generic import FormView, TemplateView

from alumnica_model.models import AuthUser
from webapp.forms.profile_forms import *


class FirstLoginInfoView(FormView):
    template_name = 'webapp/pages/first-login-info.html'
    form_class = FirstLoginInfoForm

    @method_decorator(login_required(login_url='login_view'))
    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_staff:
            return super(FirstLoginInfoView, self).dispatch(*args, **kwargs)
        else:
            return redirect('/admin/')

    def form_valid(self, form):
        user = AuthUser.objects.get(email=self.request.user.email)
        form.save_form(user)
        return redirect(to='first-login-p1_view')


class FirstLoginP1View(FormView):
    template_name = 'webapp/pages/first-login-p1.html'
    form_class = FirstLoginP1

    def form_valid(self, form):
        option_selected = form.cleaned_data.get('learning_options')
        if option_selected == '2':
            return redirect(to='first-login-p21_view')


class FirstLoginP21View(TemplateView):
    template_name = 'webapp/pages/first-login-p2.1.html'
