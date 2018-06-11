from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import View

from alumnica_model.models import ODA


class ODAView(LoginRequiredMixin, View):
    login_url = 'login_view'
    template_name = 'webapp/pages/oda.html'

    def dispatch(self, request, *args, **kwargs):
        oda = ODA.objects.get(pk=kwargs['pk'])
        return render(request, self.template_name, {'oda': oda})