import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import FormView

from alumnica_model.mixins import OnlyLearnerMixin
from alumnica_model.models import ODA
from alumnica_model.models.content import MicroODAByLearningStyle, MicroODAType
from webapp.statement_builders import access_statement_with_parent


class ODAView(LoginRequiredMixin, OnlyLearnerMixin, FormView):
    login_url = 'login_view'
    template_name = 'webapp/pages/oda.html'

    def dispatch(self, request, *args, **kwargs):
        if request.method == 'GET':
            oda = ODA.objects.get(pk=self.kwargs['pk'])
            timestamp = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc).isoformat()
            access_statement_with_parent(request=request,
                                         object_type='oda',
                                         object_name=oda.name,
                                         parent_type='materia',
                                         parent_name=oda.subject.name,
                                         tags_array=oda.tags.all(),
                                         timestamp=timestamp)
        return super(ODAView, self).dispatch(request, *args, **kwargs)

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
