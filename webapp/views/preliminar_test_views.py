import datetime
import random

from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.generic import FormView
from sweetify import sweetify

from alumnica_model.models import users, AuthUser
from alumnica_model.models.progress import LearnerLoginProgress
from webapp.forms.preliminar_test_forms import FirstLoginTestInfoForm, FirstLoginTest
from webapp.forms.user_forms import UserForm, UserLoginForm
from webapp.statement_builders import login_statement, register_statement
from webapp.tokens import account_activation_token


class LoginTestView(FormView):
    """
    Login view
    """
    form_class = UserLoginForm
    template_name = 'webapp/pages/login.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.profile.type == users.TYPE_LEARNER:
            if not request.user.profile.created_by_learner_test:
                return redirect(to='login_view')
            if request.user.first_name == "":
                return redirect(to='first_login_test_info_view')
            return redirect(to='first_login_test_p1_view')
        else:
            return super(LoginTestView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')

        timestamp = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc).isoformat()
        login_statement(request=self.request, timestamp=timestamp, user=user)
        if not self.request.user.profile.created_by_learner_test:
            return redirect(to='login_view')
        if user.first_name == "":
            return redirect(to='first_login_test_info_view')
        return redirect(to='first_login_test_p1_view')

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


class SignUpTestView(FormView):
    """
    Create new AuthUser view
    """
    form_class = UserForm
    template_name = 'webapp/pages/signup.html'
    success_url = reverse_lazy('login_test_view')

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
        user.profile.created_by_learner_test = True
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
        sweetify.success(self.request, 'Por favor confirma tu registro desde tu dirección de correo electrónico', persistent='Ok')

        return redirect(to='login_test_view')

    def form_invalid(self, form):
        if form['password'].errors:
            sweetify.error(self.request, form.errors['password'][0], persistent='Ok')
        elif form['email'].errors:
            sweetify.error(self.request, form.errors['email'][0], persistent='Ok')
        context = self.get_context_data()
        return self.render_to_response(context)


class FirstLoginTestInfoView(LoginRequiredMixin, FormView):
    login_url = 'login_test_view'
    template_name = 'webapp/pages/first-login-info.html'
    form_class = FirstLoginTestInfoForm

    def form_valid(self, form):
        user = AuthUser.objects.get(email=self.request.user.email)
        form.save_form(user)
        timestamp = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc).isoformat()
        register_statement(request=self.request, timestamp=timestamp, user=user)
        return redirect(to='first_login_test_p1_view')


class FirstLoginTestP1View(LoginRequiredMixin, FormView):
    """
    Short Learning style quiz view
    """
    login_url = 'login_test_view'
    template_name = 'webapp/pages/first-login-p1.html'
    form_class = FirstLoginTest
    first_selection = '0'
    second_selection = '0'

    def form_valid(self, form):
        self.first_selection = self.request.POST.get('pregunta-2set')
        self.second_selection = self.request.POST.get('pregunta-3set')
        form.save_form(self.request.user, self.first_selection, self.second_selection)
        return redirect(to='logout_view')


class SignUpTestConfirmation(FormView):

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
                return redirect(to='login_test_view')
            else:
                return redirect(to='confirmation_test_error_view', pk=user.pk)
        else:
            sweetify.error(self.request, 'El link es inválido', persistent='Ok')
            return redirect(to='login_test_view')


class SignupTestConfirmationError(FormView):
    template_name = 'webapp/pages/account_active_error.html'

    def get_context_data(self, **kwargs):
        user = AuthUser.objects.get(pk=self.kwargs['pk'])
        context = {'user': user}
        return context

    def post(self, request, *args, **kwargs):
        user = AuthUser.objects.get(pk=self.kwargs['pk'])
        current_site = get_current_site(self.request)
        mail_subject = 'Activa tu cuenta de Alúmnica.'
        message = render_to_string('webapp/partials/active_test_email.html', {
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

        return redirect(to='login_test_view')
