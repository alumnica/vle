from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import FormView, TemplateView

from alumnica_model.models import Ambit


class AmbitGridView(LoginRequiredMixin, FormView):
    login_url = 'login_view'
    template_name = 'webapp/pages/ambitos-grid.html'

    def get(self, request, *args, **kwargs):
        ambits_list= Ambit.objects.all().filter(is_published=True).order_by('position')

        return render(self.request, self.template_name, {'ambits_list': ambits_list})


class TestView(TemplateView):
    template_name = 'webapp/pages/test.html'