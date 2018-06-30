from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import View

from alumnica_model.models import ODA


class ODAView(LoginRequiredMixin, View):
    login_url = 'login_view'
    template_name = 'webapp/pages/oda.html'

    def dispatch(self, request, *args, **kwargs):
        oda = ODA.objects.get(pk=kwargs['pk'])
        microodas_list = oda.microodas.order_by('default_position')
        moments_list = []
        for microoda in microodas_list:
            moments = microoda.activities.order_by('default_position')
            moments_list.append(moments)

        microodas_moments = zip(microodas_list, moments_list)

        return render(request, self.template_name, {'oda': oda, 'microodas_moments': microodas_moments})
