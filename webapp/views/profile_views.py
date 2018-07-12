
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import FormView

from alumnica_model.mixins import OnlyLearnerMixin
from alumnica_model.models import AuthUser
from webapp.forms.profile_forms import *


class FirstLoginInfoView(LoginRequiredMixin, OnlyLearnerMixin, FormView):
    login_url = 'login_view'
    template_name = 'webapp/pages/first-login-info.html'
    form_class = FirstLoginInfoForm

    def form_valid(self, form):
        user = AuthUser.objects.get(email=self.request.user.email)
        form.save_form(user)
        return redirect(to='first-login-p1_view')


class FirstLoginP1View(LoginRequiredMixin, OnlyLearnerMixin, FormView):
    login_url = 'login_view'
    template_name = 'webapp/pages/first-login-p1.html'
    form_class = FirstLoginP1

    def form_valid(self, form):
        option_selected = self.request.POST.get('pregunta-1set')
        if option_selected == '1':
            return redirect(to='first-login-p2_view')
        elif option_selected == '2':
            return redirect(to='first-login-p3_view')


class FirstLoginP2View(LoginRequiredMixin, OnlyLearnerMixin, FormView):
    login_url = 'login_view'
    template_name = 'webapp/pages/first-login-p2.1.html'
    form_class = FirstLoginP2
    first_selection = '0'
    second_selection = '0'

    def form_valid(self, form):
        self.first_selection = self.request.POST.get('pregunta-2set')
        self.second_selection = self.request.POST.get('pregunta-3set')
        form.save_form(self.request.user, self.first_selection, self.second_selection)
        return redirect(to='dashboard_view')


class FirstLoginP3View(LoginRequiredMixin, OnlyLearnerMixin, FormView):
    login_url = 'login_view'
    template_name = 'webapp/pages/first-login-p3.1.html'
    form_class = FirstLoginP3
    first_selection = '0'
    second_selection = '0'

    def form_valid(self, form):
        self.first_selection = self.request.POST.get('pregunta-2set')
        self.second_selection = self.request.POST.get('pregunta-3set')
        form.save_form(self.request.user, self.first_selection, self.second_selection)
        return redirect(to='dashboard_view')