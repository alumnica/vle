from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import FormView, UpdateView
from sweetify import sweetify

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


class LargeLearningStyleQuizView(LoginRequiredMixin, OnlyLearnerMixin, FormView):
    login_url = 'login_view'
    form_class = LargeLeraningStyleQuizForm
    template_name = 'webapp/pages/user-test.html'

    def form_valid(self, form):
        answers = self.request.POST['test-answers'].split(',')
        letters = {'a': 0, 'b': 1, 'c': 2, 'd': 3}
        answers_numbers = [0, 0, 0, 0]
        for answer in answers:
            answers_numbers[letters[answer]] += 1

        if answers_numbers[0] > answers_numbers[1] and answers_numbers[3] > answers_numbers[2]:
            self.request.user.profile.learning_style = LearningStyle.objects.get(name='Acomodador')
        elif answers_numbers[1] > answers_numbers[0] and answers_numbers[2] > answers_numbers[3]:
            self.request.user.profile.learning_style = LearningStyle.objects.get(name='Asimilador')
        elif answers_numbers[0] > answers_numbers[1] and answers_numbers[2] > answers_numbers[3]:
            self.request.user.profile.learning_style = LearningStyle.objects.get(name='Divergente')
        elif answers_numbers[1] > answers_numbers[2] and answers_numbers[3] > answers_numbers[2]:
            self.request.user.profile.learning_style = LearningStyle.objects.get(name='Convergente')

        self.request.user.profile.large_quiz_completed = True
        self.request.user.profile.save()

        return redirect(to='dashboard_view')


class ProfileSettingsView(LoginRequiredMixin, OnlyLearnerMixin, UpdateView):
    login_url = 'login_view'
    template_name = 'webapp/pages/user-profile.html'
    form_class = ProfileSettingsForm

    def get_object(self, queryset=None):
        return self.request.user

    def form_invalid(self, form):
        if form['new_password'].errors:
            sweetify.error(self.request, form.errors['new_password'][0], persistent='Ok')
        elif form['new_password_confirmation'].errors:
            sweetify.error(self.request, form.errors['new_password_confirmation'][0], persistent='Ok')
        elif form['previous_password'].errors:
            sweetify.error(self.request, form.errors['previous_password'][0], persistent='Ok')

        context = self.get_context_data()
        return render(self.request, self.template_name, context=context)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('profile_view')