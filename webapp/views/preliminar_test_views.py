import datetime
import random

from django.contrib.auth import login
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.generic import FormView, TemplateView
from sweetify import sweetify

from alumnica_model.mixins import OnlyTestLearnerMixin
from alumnica_model.models import users, AuthUser
from alumnica_model.models.content import LearningStyle
from webapp.forms.preliminar_test_forms import FirstLoginTestInfoForm, FirstLoginTest
from webapp.forms.user_forms import UserForm
from webapp.gamification import EXPERIENCE_POINTS_CONSTANTS
from webapp.statement_builders import register_statement, learning_experience_received, \
    access_statement
from webapp.tokens import account_activation_token


class SignUpTestView(FormView):
    """
    Create new AuthUser view
    """
    form_class = UserForm
    template_name = 'webapp/pages/signup.html'
    success_url = reverse_lazy('first_login_test_info_view')

    def form_valid(self, form):
        avatar_options = ['A', 'B', 'C', 'D']
        user = form.save(commit=False)
        user.is_active = False
        user.user_type = users.TYPE_LEARNER
        user.save()
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
        login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')
        sweetify.success(self.request, 'Por favor confirma tu registro desde tu dirección de correo electrónico',
                         persistent='Ok')

        return redirect(to='first_login_test_info_view', pk=user.pk)

    def form_invalid(self, form):
        if form['password'].errors:
            sweetify.error(self.request, form.errors['password'][0], persistent='Ok')
        elif form['email'].errors:
            sweetify.error(self.request, form.errors['email'][0], persistent='Ok')
        context = self.get_context_data()
        return self.render_to_response(context)


class FirstLoginTestInfoView(OnlyTestLearnerMixin, FormView):
    login_url = 'login_view'
    template_name = 'webapp/pages/first-login-info.html'
    form_class = FirstLoginTestInfoForm

    def form_valid(self, form):
        user = AuthUser.objects.get(pk=self.kwargs['pk'])
        form.save_form(user)
        timestamp = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc).isoformat()
        register_statement(request=self.request, timestamp=timestamp, user=user)
        return redirect(to='first_login_test_p1_view', pk=user.pk)


class FirstLoginTestP1View(OnlyTestLearnerMixin, FormView):
    """
    Short Learning style quiz view
    """
    login_url = 'login_view'
    template_name = 'webapp/pages/user-test-competencias.html'
    form_class = FirstLoginTest
    first_selection = '0'
    second_selection = '0'

    def dispatch(self, request, *args, **kwargs):
        response = super(FirstLoginTestP1View, self).dispatch(request, *args, **kwargs)
        if response.status_code == 200 and request.method == 'GET':
            user = AuthUser.objects.get(pk=self.kwargs['pk'])
            if response.status_code == 200 and request.method == 'GET':
                timestamp = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc).isoformat()
                access_statement(user, 'Large Learning Style Quiz', timestamp)
        return response

    def form_valid(self, form):
        answers = self.request.POST['test-answers'].split(',')
        letters = {'a': 0, 'b': 1, 'c': 2, 'd': 3}
        answers_numbers = [0, 0, 0, 0]
        for answer in answers:
            answers_numbers[letters[answer]] += 1

        user = AuthUser.objects.get(pk=self.kwargs['pk'])

        if answers_numbers[0] > answers_numbers[1] and answers_numbers[3] > answers_numbers[2]:
            user.profile.learning_style = LearningStyle.objects.get(name='Acomodador')
        elif answers_numbers[1] > answers_numbers[0] and answers_numbers[2] > answers_numbers[3]:
            user.profile.learning_style = LearningStyle.objects.get(name='Asimilador')
        elif answers_numbers[0] > answers_numbers[1] and answers_numbers[2] > answers_numbers[3]:
            user.profile.learning_style = LearningStyle.objects.get(name='Divergente')
        elif answers_numbers[1] > answers_numbers[2] and answers_numbers[3] > answers_numbers[2]:
            user.profile.learning_style = LearningStyle.objects.get(name='Convergente')
        timestamp = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc).isoformat()
        learning_experience_received(user=user,
                                     object_type='Learning Style Quiz',
                                     object_name=user.profile.learning_style.name,
                                     timestamp=timestamp,
                                     gained_xp=EXPERIENCE_POINTS_CONSTANTS['learning_large_quiz'])

        user.profile.save()

        return redirect(to='confirmation_test_error_view')


class SignUpTestConfirmation(OnlyTestLearnerMixin, FormView):
    login_url = 'login_view'

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
                sweetify.success(self.request, 'Tu cuenta ha sido activada!', persistent='Ok')
                return redirect(to='first_login_test_info_view')
            else:
                return redirect(to='confirmation_test_error_view', pk=user.pk)
        else:
            sweetify.error(self.request, 'El link es inválido', persistent='Ok')
            return redirect(to='first_login_test_info_view', pk=user.pk)


class SignupTestConfirmationError(OnlyTestLearnerMixin, FormView):
    login_url = 'login_view'
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
        login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')
        return redirect(to='first_login_test_info_view', pk=user.pk)


class TestAnswered(TemplateView):
    template_name = 'webapp/pages/test_answered.html'
