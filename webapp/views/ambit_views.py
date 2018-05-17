from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import FormView

from alumnica_model.models import AmbitModel


class AmbitGridView(LoginRequiredMixin, FormView):
    login_url = 'login_view'
    template_name = 'webapp/pages/ambitos-grid.html'

    def get(self, request, *args, **kwargs):
        ambits_list_raw = AmbitModel.objects.all().filter(is_published_field=True)
        ambits_list = ['na']*30

        for ambit in ambits_list_raw:
            ambits_list[ambit.position-1] = ambit

        return render(self.request, self.template_name, {'ambits_list': ambits_list})
