from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import *
from django.views.generic.base import TemplateView
from alumnica_model.alumnica_entities.users import UserType
from webapp.forms.user_forms import UserForm, UserLoginForm


class IndexView(TemplateView):
    template_name = 'webapp/pages/index.html'


class LoginView(FormView):
    form_class = UserLoginForm
    template_name = 'webapp/pages/login.html'

    def dispatch(self, request, *args, **kwargs):
        print('dispatch!')
        if request.user.is_authenticated and not request.user.is_staff:
            return redirect(to='dashboard_view')
        else:
            print('dispatch not autheticated')
            return super(LoginView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        login(self.request, form.get_user())
        return redirect(to='dashboard_view')


class SignUpView(FormView):
    form_class = UserForm
    template_name = 'webapp/pages/signup.html'
    success_url = reverse_lazy('index_view')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.user_type = UserType.LEARNER
        user.save()
        login(self.request, user)
        return redirect(to='login_view')


class DashboardView(TemplateView):
    template_name = 'webapp/pages/dashboard.html'

    @method_decorator(login_required(login_url='login_view'))
    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_staff:
            return super(DashboardView, self).dispatch(*args, **kwargs)
        else:
            return redirect('/admin/')


class LogoutView(RedirectView):
    pattern_name = 'login_view'

    def get(self, request, *args, **kwargs):
        logout(request)
        return super(LogoutView, self).get(request, *args, **kwargs)