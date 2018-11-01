import datetime
import random

from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.generic import *
from django.views.generic.base import TemplateView
from sweetify import sweetify

from alumnica_model.mixins import OnlyLearnerMixin, LoginCounterMixin
from alumnica_model.models import users, Ambit, AuthUser
from alumnica_model.models.progress import LearnerLoginProgress
from webapp.forms.user_forms import UserForm, UserLoginForm
from webapp.gamification import get_learner_level
from webapp.statement_builders import login_statement, logout_statement
from webapp.tokens import account_activation_token


class LandingPageView(TemplateView):
    """
    Landing view
    """
    template_name = 'webapp/pages/landing.html'


class IndexView(TemplateView):
    """
    Home view
    """
    template_name = 'webapp/pages/index.html'


class LoginView(FormView):
    """
    Login view
    """
    form_class = UserLoginForm
    template_name = 'webapp/pages/login.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.profile.type == users.TYPE_LEARNER:
            if request.user.profile.created_by_learner_test:
                return redirect(to='first_login_test_p1_view')
            if request.user.first_name == "":
                return redirect(to='first-login-info_view')
            if request.user.profile.learning_style is None:
                return redirect(to='first-login-p1_view')
            return redirect(to='dashboard_view')
        else:
            return super(LoginView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')

        timestamp = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc).isoformat()
        login_statement(request=self.request, timestamp=timestamp, user=user)
        if self.request.user.profile.created_by_learner_test:
            return redirect(to='first_login_test_p1_view')
        if user.first_name == "":
            return redirect(to='first-login-info_view')
        if self.request.user.profile.learning_style is None:
            return redirect(to='first-login-p1_view')
        return redirect(to='dashboard_view')

    def form_invalid(self, form):
        if form['email'].errors:
            if form.errors['email'].data[0].code == 'account_activation_error':
                user = AuthUser.objects.get(email=form.data['email'])
                return redirect(to='confirmation_error_view', pk=user.pk)
            sweetify.error(self.request, form.errors['email'][0], persistent='Ok')
        elif form['password'].errors:
            sweetify.error(self.request, form.errors['password'][0], persistent='Ok')
        context = self.get_context_data()
        return self.render_to_response(context)


class SignUpView(FormView):
    """
    Create new AuthUser view
    """
    form_class = UserForm
    template_name = 'webapp/pages/signup.html'
    success_url = reverse_lazy('index_view')

    def form_valid(self, form):
        avatar_options = ['A', 'B', 'C', 'D']
        user = form.save(commit=False)
        user.is_active = False
        user.user_type = users.TYPE_LEARNER
        user.save()
        user.profile.login_progress = LearnerLoginProgress.objects.create(login_counter=1,
                                                                          last_activity=datetime.datetime.now(),
                                                                          first_activity=datetime.datetime.now())
        for option in avatar_options:
            user.profile.avatar_progresses.create(avatar_name=option)
        avatar = user.profile.avatar_progresses.get(avatar_name=random.choice(avatar_options))
        avatar.active = True
        avatar.save()
        user.profile.save()
        current_site = get_current_site(self.request)
        mail_subject = 'Activate your blog account.'
        message = render_to_string('webapp/partials/active_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode("utf-8"),
            'token': account_activation_token.make_token(user),
        })
        to_email = form.cleaned_data.get('email')
        email = EmailMessage(
            mail_subject, message, to=[to_email]
        )
        email.send()
        sweetify.success(self.request, 'Por favor confirma tu registro desde tu dirección de correo electrónico',
                         persistent='Ok')

        return redirect(to='login_view')

    def form_invalid(self, form):
        if form['password'].errors:
            sweetify.error(self.request, form.errors['password'][0], persistent='Ok')
        elif form['email'].errors:
            sweetify.error(self.request, form.errors['email'][0], persistent='Ok')
        context = self.get_context_data()
        return self.render_to_response(context)


class DashboardView(LoginRequiredMixin, OnlyLearnerMixin, LoginCounterMixin, FormView):
    """
    User dashboard view
    """
    template_name = 'webapp/pages/dashboard.html'
    login_url = 'login_view'

    def dispatch(self, request, *args, **kwargs):
        response = super(DashboardView, self).dispatch(request, *args, **kwargs)
        if response.status_code == 200:
            if request.user.first_name == "" or request.user.last_name == "" or \
                    request.user.profile.birth_date is None or request.user.profile.gender == "":
                return redirect(to='first-login-info_view')
            if request.user.profile.learning_style is None:
                return redirect(to='first-login-p1_view')
        return response

    def get_context_data(self, **kwargs):
        user = self.request.user
        level = get_learner_level(user.profile.experience_points)
        context = {'user': self.request.user, 'level': level}
        activities = []
        for activity in user.profile.recent_activities.order_by('pk')[0:3]:
            activities.append([activity.oda, activity.oda.subject])
        ambits = Ambit.objects.exclude(is_published=False)
        context.update({'recent_activities': activities, 'ambits': ambits})

        return context


class LogoutView(RedirectView):
    """
    Logout redirecting view
    """
    pattern_name = 'login_view'

    def get(self, request, *args, **kwargs):
        timestamp = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc).isoformat()
        logout_statement(request=self.request, timestamp=timestamp, user=request.user)
        logout(request)
        return super(LogoutView, self).get(request, *args, **kwargs)


class SignUpConfirmation(FormView):

    def get(self, request, *args, **kwargs):
        uidb64 = (self.kwargs['uidb64']).encode()
        token = self.kwargs['token']

        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = AuthUser.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, AuthUser.DoesNotExist):
            user = None
        if user is not None:
            if account_activation_token.check_token(user, token):
                user.is_active = True
                user.save()
                login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')
                sweetify.success(self.request, 'Tu cuenta ha sido activada!', persistent='Ok')
                return redirect(to='login_view')
            else:
                return redirect(to='confirmation_error_view', pk=user.pk)
        else:
            sweetify.error(self.request, 'El link es inválido', persistent='Ok')
            return redirect(to='login_view')


class SignupConfirmationError(FormView):
    template_name = 'webapp/pages/account_active_error.html'

    def get_context_data(self, **kwargs):
        user = AuthUser.objects.get(pk=self.kwargs['pk'])
        context = {'user': user}
        return context

    def post(self, request, *args, **kwargs):
        user = AuthUser.objects.get(pk=self.kwargs['pk'])
        current_site = get_current_site(self.request)
        mail_subject = 'Activa tu cuenta de Alúmnica.'
        message = render_to_string('webapp/partials/active_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode("utf-8"),
            'token': account_activation_token.make_token(user),
        })
        to_email = user.email
        email = EmailMessage(
            mail_subject, message, to=[to_email]
        )
        email.send()
        sweetify.success(self.request, 'Por favor confirma tu registro desde tu dirección de correo electrónico',
                         persistent='Ok')

        return redirect(to='login_view')
