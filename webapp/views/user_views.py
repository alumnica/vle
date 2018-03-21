from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import FormView
from django.views.generic.base import TemplateView, View

from alumnica_model.alumnica_entities.users import UserType
from webapp.forms.user_forms import UserForm


class IndexView(TemplateView):
    template_name = 'webapp/pages/index.html'


class LoginView(View):
    def dispatch(self, request, *args, **kwargs):
        return redirect(to='index_view')


class SignUpView(FormView):
    form_class = UserForm
    template_name = 'webapp/pages/signup.html'
    success_url = reverse_lazy('index_view')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.user_type = UserType.LEARNER
        user.save()
        return super(SignUpView, self).form_valid(form)
