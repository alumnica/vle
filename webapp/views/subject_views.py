import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import FormView

from alumnica_model.mixins import OnlyLearnerMixin
from alumnica_model.models import Subject
from webapp.statement_builders import access_statement_with_parent


class SubjectView(LoginRequiredMixin, OnlyLearnerMixin, FormView):
    """
    ODAs per sections in subject view
    """
    login_url = 'login_view'
    template_name = 'webapp/pages/materia.html'
    model = Subject

    def dispatch(self, request, *args, **kwargs):
        if request.method == 'GET':
            subject = Subject.objects.get(pk=self.kwargs['pk'])
            timestamp = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc).isoformat()
            access_statement_with_parent(request=request,
                                         object_type='materia',
                                         object_name=subject.name,
                                         parent_type='ambito',
                                         parent_name=subject.ambit.name,
                                         tags_array=subject.tags.all(),
                                         timestamp=timestamp)
        return super(SubjectView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        subject = Subject.objects.get(pk=self.kwargs['pk'])
        odas_list = []
        odas_states = []
        odas_microodas_completed = []
        for oda in subject.odas.all():
            moments_state, microodas_completed = oda.get_oda_status(self.request.user.profile)
            if oda.is_evaluation_complete(self.request.user.profile) and moments_state == 'completed':
                state = 'finalized'
            else:
                state = moments_state
            odas_list.append(oda)
            odas_states.append(state)
            odas_microodas_completed.append(microodas_completed)
        zones = ['a', 'b', 'c', 'd']
        odas_zip = zip(odas_list, odas_states, odas_microodas_completed)
        subject_zip = zip(subject.sections_images.all(), zones[0:subject.number_of_sections])

        return {'subject': subject, 'subject_zip': subject_zip, 'odas_zip': odas_zip}
