from django.views.generic.base import TemplateView, View


class IndexView(TemplateView):
    template_name = 'webapp/pages/index.html'

class SignUpView(View):
    pass

class LoginView(View):
    pass