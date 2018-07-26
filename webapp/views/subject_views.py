from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import DetailView, FormView
from django.views.generic.base import View

from alumnica_model.mixins import OnlyLearnerMixin
from alumnica_model.models import Subject


class SubjectView(LoginRequiredMixin, OnlyLearnerMixin,  FormView):
    login_url = 'login_view'
    template_name = 'webapp/pages/materia.html'
    model = Subject

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