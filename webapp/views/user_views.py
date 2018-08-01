import datetime

from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import *
from django.views.generic.base import TemplateView
from sweetify import sweetify

from alumnica_model.mixins import OnlyLearnerMixin
from alumnica_model.models import users, Ambit
from alumnica_model.models.users import TYPE_LEARNER
from webapp.forms.user_forms import UserForm, UserLoginForm
from webapp.statement_builders import login_statement, logout_statement


class LandingPageView(TemplateView):
    template_name = 'webapp/pages/landing.html'


class IndexView(TemplateView):
    template_name = 'webapp/pages/index.html'


class LoginView(FormView):
    form_class = UserLoginForm
    template_name = 'webapp/pages/login.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.profile == users.TYPE_LEARNER:
            if request.user.first_name == "":
                return redirect(to='first-login-info_view')
            if request.user.profile.learning_style is None:
                return redirect(to='first-login-p1_view')
            return redirect(to='dashboard_view')
        else:
            return super(LoginView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)

        timestamp = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc).isoformat()
        login_statement(request=self.request, timestamp=timestamp, user=user)

        if user.first_name == "":
            return redirect(to='first-login-info_view')
        if self.request.user.profile.learning_style is None:
            return redirect(to='first-login-p1_view')
        return redirect(to='dashboard_view')

    def form_invalid(self, form):
        sweetify.error(self.request, form.errors['password'][0], persistent='Ok')
        context = self.get_context_data()
        return self.render_to_response(context)


class SignUpView(FormView):
    form_class = UserForm
    template_name = 'webapp/pages/signup.html'
    success_url = reverse_lazy('index_view')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.user_type = users.TYPE_LEARNER
        user.save()
        login(self.request, user)

        return redirect(to='first-login-info_view')

    def form_invalid(self, form):
        if form['password'].errors:
            sweetify.error(self.request, form.errors['password'][0], persistent='Ok')
        elif form['email'].errors:
            sweetify.error(self.request, form.errors['email'][0], persistent='Ok')
        context = self.get_context_data()
        return self.render_to_response(context)


class DashboardView(LoginRequiredMixin, OnlyLearnerMixin, FormView):
    template_name = 'webapp/pages/dashboard.html'
    login_url = 'login_view'

    def get_context_data(self, **kwargs):
        user = self.request.user
        context = {'user': self.request.user}
        activities = []
        for activity in user.profile.recent_activities.order_by('pk')[0:3]:
            activities.append([activity, activity.subject])
        ambits = Ambit.objects.exclude(is_published=False)
        context.update({'recent_activities': activities, 'ambits':ambits})

        return context


class LogoutView(RedirectView):
    pattern_name = 'login_view'

    def get(self, request, *args, **kwargs):
        timestamp = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc).isoformat()
        logout_statement(request=self.request, timestamp=timestamp, user=request.user)
        logout(request)
        return super(LogoutView, self).get(request, *args, **kwargs)
