from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import FormView

from alumnica_model.models import Moment, LearnerProgressInActivity


class MomentView(LoginRequiredMixin, FormView):
    login_url = "login_view"
    template_name = "webapp/pages/momentos.html"

    def get_context_data(self, **kwargs):
        moment_instance = Moment.objects.get(pk=self.kwargs['pk'])
        learner = self.request.user.profile
        learner.assign_recent_oda(moment_instance.microoda.oda)
        learner.microoda_in_progress = moment_instance.microoda
        learner.save()

        moment_array = moment_instance.microoda.activities.all()

        for moment in moment_array:
            if not learner.activities_progresses.filter(activity=moment).exists():
                progress = LearnerProgressInActivity.objects.create(activity=moment, score=0, is_complete=False)
                learner.activities_progresses.add(progress)

        return {'moment_array': moment_array}