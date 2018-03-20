from django.shortcuts import redirect, render
from django.views.generic.base import TemplateView, View
from webapp.forms.user_forms import LearnerForm, UserForm


class IndexView(TemplateView):
    template_name = 'webapp/pages/index.html'

class LoginView(View):
    pass

class SignUpView(View):
    user_form_class = UserForm
    learner_form_class = LearnerForm

    template_name = 'webapp/pages/signup.html'

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('/users/profile')
        user_form = self.user_form_class(None)
        learner_form = self.learner_form_class(None)

        return render(request, self.template_name,
                      {'user_form': user_form, 'learner_form': learner_form})

    def post(self, request, *args, **kwargs):
        password = request.POST['password1']
        password2 = request.POST['password2']
        print(password)
        print(password2)
        if password != password2:
            user_form = self.user_form_class(data=request.POST)
            learner_form = self.learner_form_class(data=request.POST)
            return render(request, "webapp/pages/signup.html", {'user_form': user_form, 'learner_form': learner_form})
        user_form = UserForm(data=request.POST)
        user = user_form.save(commit=False)

        if user_form.is_valid:
            user.set_password(password)
            user.save()

            return redirect('/users/login_view')

        return redirect(request, *args, **kwargs)