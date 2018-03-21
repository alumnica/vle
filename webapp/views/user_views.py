from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.views.generic.base import TemplateView, View, RedirectView

from alumnica_model.models import AuthUser
from webapp.forms.user_forms import LearnerForm, UserForm, UserLoginForm


class IndexView(TemplateView):
    template_name = 'webapp/pages/index.html'


class LoginView(View):
    class LoginView(View):
        form_class = UserLoginForm
        template_name = "studio/pages/login.html"
        success_url = '/users/profile/'

        def get(self, request):
            if request.user.is_authenticated and not request.user.is_staff:
                return HttpResponseRedirect('/users/profile')
            else:
                form = UserLoginForm(None)
                return render(request, "studio/pages/login.html", {'form': form})

        def post(self, request):
            form = UserLoginForm(data=request.POST)
            if form.is_valid:
                username = request.POST['username']
                password = request.POST['password']
                try:
                    user = AuthUser.objects.get(username=username)
                    print(username)
                    print(password)

                    if user.check_password(password) and not user.is_staff:
                        login(request, user)
                        return redirect('/users/profile')
                except AuthUser.DoesNotExist:
                    form = UserLoginForm(None)
                    return render(request, "webapp/pages/login.html", {'form': form})

            print('form not valid')
            form = UserLoginForm(None)
            return render(request, "webapp/pages/login.html", {'form': form})

class LogoutView(RedirectView):
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