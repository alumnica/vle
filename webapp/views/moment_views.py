import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.datastructures import OrderedSet
from django.utils.decorators import method_decorator
from django.views.decorators.clickjacking import xframe_options_exempt
from django.views.generic import FormView, DetailView
from alumnica_model.models import Moment, LearnerProgressInActivity
from alumnica_model.models.h5p import H5Package


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


@method_decorator(xframe_options_exempt, name='dispatch')
class H5PackageView(LoginRequiredMixin, DetailView):
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

        context.update({
            'library_directory_name': self.object.main_library.full_name,
            'content_json': json.dumps(self.object.content, ensure_ascii=False),
            'stylesheets': list(OrderedSet({
                css for lib in self.object.preloaded_dependencies.all()
                for css in lib.get_all_stylesheets()
            })),
            'scripts': list(OrderedSet([
                script for lib in self.object.preloaded_dependencies.all()
                for script in lib.get_all_javascripts()
            ]))
        })

        return context

