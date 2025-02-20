import datetime
import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.datastructures import OrderedSet
from django.utils.decorators import method_decorator
from django.views.decorators.clickjacking import xframe_options_exempt
from django.views.generic import FormView, DetailView

from alumnica_model.mixins import LoginCounterMixin, OnlyLearnerMixin
from alumnica_model.models import Moment
from alumnica_model.models.h5p import H5Package
from vle_webapp.settings import AWS_INSTANCE_URL
from webapp.gamification import uoda_completed_xp
from webapp.statement_builders import access_statement_with_parent


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
            access_statement_with_parent(request=request,
                                         object_type='uoda',
                                         object_name=moment.microoda.name,
                                         parent_type='oda',
                                         parent_name=moment.microoda.oda.name,
                                         tags_array=moment.tags.all(),
                                         timestamp=timestamp)
        return response

    def get_context_data(self, **kwargs):
        moment_instance = Moment.objects.get(pk=self.kwargs['pk'])
        learner = self.request.user.profile
        learner.assign_recent_oda(moment_instance.microoda.oda)
        learner.microoda_in_progress = moment_instance.microoda
        learner.save()
        oda_sequence, created = learner.odas_sequence_progresses.get_or_create(oda=moment_instance.microoda.oda)

        moment_array = moment_instance.microoda.activities.all()

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


@method_decorator(xframe_options_exempt, name='dispatch')
class H5PackageView(LoginRequiredMixin, DetailView):
    """
    H5P packages iframe view
    """
    template_name = 'webapp/partials/h5p_package_view.html'
    model = H5Package
    context_object_name = 'package'

    def get_object(self, queryset=None):
        if 'pk' in self.kwargs.keys():
            return self.model.objects.get(pk=self.kwargs['pk'])
        elif 'job_id' in self.kwargs.keys():
            return self.model.objects.get(job_id=self.kwargs['job_id'])
        else:
            raise ValueError('Neither pk nor job_id were given as parameters')

    def get_context_data(self, **kwargs):
        context = super(H5PackageView, self).get_context_data(**kwargs)
        momento_pk = Moment.objects.get(h5p_package=self.object).pk
        css_dependencies = list()
        css_instances_list = list()
        js_dependencies = list()
        js_instances_list = list()

        for lib in self.object.preloaded_dependencies.all():
            css = lib.get_all_stylesheets(aws_url=AWS_INSTANCE_URL, dependencies_instances=css_instances_list)
            js = lib.get_all_javascripts(aws_url=AWS_INSTANCE_URL, dependencies_instances=js_instances_list)

            css_dependencies.extend(css)
            js_dependencies.extend(js)

        context.update({
            'library_directory_name': self.object.main_library.full_name,
            'content_json': json.dumps(self.object.content, ensure_ascii=False),
            'stylesheets': css_dependencies,
            'scripts': js_dependencies,
            "aws_url": AWS_INSTANCE_URL,
            "mom": momento_pk,
        })

        return context
