from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import DetailView
from django.views.generic.base import View

from alumnica_model.models import Subject


class SubjectView(LoginRequiredMixin, View):
    login_url = 'login_view'
    template_name = 'webapp/pages/test.html'
    model = Subject

    def dispatch(self, request, *args, **kwargs):
        subject = Subject.objects.get(pk=self.kwargs['pk'])
        odas_list = []
        odas_states = []
        for oda in subject.odas.all():
            moments_state = oda.get_oda_status(self.request.user.profile)
            if oda.is_evaluation_complete(self.request.user.profile) and moments_state == 'completed':
                state = 'finalized'
            else:
                state = moments_state
            odas_list.append(oda)
            odas_states.append(state)

        odas_zip = zip(odas_list, odas_states)

        return render(request, self.template_name, {'subject': subject, 'odas_zip': odas_zip})