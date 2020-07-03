import datetime
import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.datastructures import OrderedSet
from django.utils.decorators import method_decorator
from django.views.decorators.clickjacking import xframe_options_exempt
from django.views.generic import FormView, DetailView

from alumnica_model.mixins import LoginCounterMixin, OnlyLearnerMixin
from alumnica_model.models import Moment
from vle_webapp.settings import AWS_INSTANCE_URL
from webapp.gamification import uoda_completed_xp


class MomentView(LoginRequiredMixin, OnlyLearnerMixin, LoginCounterMixin, FormView):
    """
    MicroODA activities obtained by Momento pk view
    """
    login_url = "login_view"
    template_name = "webapp/pages/momentos.html"

    def dispatch(self, request, *args, **kwargs):
        response = super(MomentView, self).dispatch(request, *args, **kwargs)
        if response.status_code == 200 and request.method == 'GET':
            moment = Moment.objects.get(pk=self.kwargs['pk'])
            
            timestamp = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc).isoformat()
        return response

    def get_context_data(self, **kwargs):
        moment_instance = Moment.objects.get(pk=self.kwargs['pk'])
        learner = self.request.user.profile
        learner.assign_recent_oda(moment_instance.microoda.oda)
        learner.microoda_in_progress = moment_instance.microoda
        learner.save()
        oda_sequence, created = learner.odas_sequence_progresses.get_or_create(oda=moment_instance.microoda.oda)

        moment_array = moment_instance.microoda.activities.all().order_by('default_position')

        for moment in moment_array:
            if not learner.activities_progresses.filter(activity=moment).exists():
                learner.activities_progresses.create(activity=moment, score=0, is_complete=False)
        if moment_instance.microoda.type.name not in oda_sequence.uoda_progress_order:
            oda_sequence_string = "{} {}".format(oda_sequence.uoda_progress_order, moment_instance.microoda.type.name)
        else:
            oda_sequence_string = oda_sequence.uoda_progress_order

        points, equation = uoda_completed_xp(login_counter=learner.login_progress.login_counter,
                                             oda_sequencing=oda_sequence_string,
                                             learning_style=learner.learning_style.name,
                                             completed_counter=(learner.activities_progresses.filter(
                                                 activity=moment_instance).first().activity_completed_counter + 1))        
        return {'moment_array': moment_array, 'points': round(points), 'equation': equation}


