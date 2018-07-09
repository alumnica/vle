from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import View
from django.views.generic import FormView

from alumnica_model.mixins import OnlyLearnerMixin
from alumnica_model.models import ODA


class ODAView(LoginRequiredMixin, OnlyLearnerMixin, FormView):
    login_url = 'login_view'
    template_name = 'webapp/pages/oda.html'

    def get_context_data(self, **kwargs):
        oda = ODA.objects.get(pk=self.kwargs['pk'])
        microodas = oda.microodas.order_by('default_position')
        moments_list = []
        microodas_list = []

        for microoda in microodas:
            moments = microoda.activities.order_by('default_position')
            moments_list.append(moments)
            state = 'incomplete'
            if microoda.get_status_by_learner(self.request.user.profile):
                state = 'complete'
            microodas_list.append([microoda, state])

        microodas_moments = zip(microodas_list, moments_list)

        return {'oda': oda, 'microodas_moments': microodas_moments}
