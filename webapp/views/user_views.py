<<<<<<< HEAD
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.views.generic.base import TemplateView, View, RedirectView

from alumnica_model.models import AuthUser
from webapp.forms.user_forms import LearnerForm, UserForm, UserLoginForm
=======
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import FormView
from django.views.generic.base import TemplateView, View

from alumnica_model.alumnica_entities.users import UserType
from webapp.forms.user_forms import UserForm
>>>>>>> da9c0a46540845372681e37725917f818122afbf


class IndexView(TemplateView):
    template_name = 'webapp/pages/index.html'


class LoginView(View):
<<<<<<< HEAD
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
=======
    def dispatch(self, request, *args, **kwargs):
        return redirect(to='index_view')
>>>>>>> da9c0a46540845372681e37725917f818122afbf


class SignUpView(FormView):
    form_class = UserForm
    template_name = 'webapp/pages/signup.html'
    success_url = reverse_lazy('index_view')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.user_type = UserType.LEARNER
        user.save()
        return super(SignUpView, self).form_valid(form)
