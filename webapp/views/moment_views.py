import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.datastructures import OrderedSet
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
        packages_dependencies = []
        packages = []
        moment_array = moment_instance.microoda.activities.all()

        for moment in moment_array:
            packages.append(moment.h5p_package)
            packages_dependencies.append(self.get_package_dependencies(moment))
            if not learner.activities_progresses.filter(activity=moment).exists():
                progress = LearnerProgressInActivity.objects.create(activity=moment, score=0, is_complete=False)
                learner.activities_progresses.add(progress)

        moment_zip = zip(moment_array, packages_dependencies, packages)
        return {'moment_zip': moment_zip, 'microoda': moment_instance.microoda}

    def get_package_dependencies(self, moment):
        dependencies = {
            'library_directory_name': moment.h5p_package.main_library.full_name,
            'content_json': json.dumps(moment.h5p_package.content, ensure_ascii=False),
            'stylesheets': list(OrderedSet({
                css for lib in moment.h5p_package.preloaded_dependencies.all()
                for css in lib.get_all_stylesheets()
            })),
            'scripts': list(OrderedSet([
                script for lib in moment.h5p_package.preloaded_dependencies.all()
                for script in lib.get_all_javascripts()
            ]))
        }

        return dependencies

