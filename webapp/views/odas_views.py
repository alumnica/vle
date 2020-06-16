import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import FormView

from alumnica_model.mixins import OnlyLearnerMixin, LoginCounterMixin
from alumnica_model.models import ODA
from alumnica_model.models.content import MicroODAByLearningStyle, MicroODAType


class ODAView(LoginRequiredMixin, OnlyLearnerMixin, LoginCounterMixin, FormView):
    """
    MicroODAs and Momentos icons visualization assigned to ODA
    """
    login_url = 'login_view'
    template_name = 'webapp/pages/oda.html'

    def dispatch(self, request, *args, **kwargs):
        response = super(ODAView, self).dispatch(request, *args, **kwargs)
        if response.status_code == 200 and request.method == 'GET':
            oda = ODA.objects.get(pk=self.kwargs['pk'])
            timestamp = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc).isoformat()
        return response

    def get_context_data(self, **kwargs):
        oda = ODA.objects.get(pk=self.kwargs['pk'])
        microodas = []
        for uoda in MicroODAByLearningStyle[self.request.user.profile.learning_style.name]:
            microodas.append(oda.microodas.get(type=MicroODAType.objects.get(name=uoda)))
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
