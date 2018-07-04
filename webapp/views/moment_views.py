from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import FormView

from alumnica_model.models import Moment, LearnerProgressInActivity


class MomentView(LoginRequiredMixin, FormView):
    login_url = "login_view"
    template_name = "webapp/pages/momentos.html"

    def dispatch(self, request, *args, **kwargs):
        moment_instance = Moment.objects.get(pk=kwargs['pk'])
        self.request.user.profile.assign_recent_oda(moment_instance.microodas.all()[0].oda)
        moment_array = moment_instance.microodas.all()[0].activities.all()
        learner = request.user.profile
        for moment in moment_array:
            if not learner.activities_progresses.filter(activity=moment).exists():
                progress = LearnerProgressInActivity.objects.create(activity=moment, score=0, is_complete=False)
                learner.activities_progresses.add(progress)

        return render(request, self.template_name, {'moment_array': moment_array}) 