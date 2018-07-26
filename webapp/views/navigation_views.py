from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views import View
from django.views.generic import RedirectView, FormView

from alumnica_model.mixins import OnlyLearnerMixin
from alumnica_model.models import ODA, Tag


class RecentActivitiesView(LoginRequiredMixin, OnlyLearnerMixin, FormView):
    login_url = 'login_view'
    template_name = 'webapp/pages/recent.html'

    def get_context_data(self, **kwargs):
        odas_list = []

        for activity_progress in self.request.user.profile.activities_progresses.all():
            if activity_progress.activity.microoda.oda not in odas_list:
                odas_list.append(activity_progress.activity.microoda.oda)

        return {'odas_list': odas_list}


class SearchView(LoginRequiredMixin, OnlyLearnerMixin, FormView):
    login_url = 'login_view'
    template_name = 'webapp/pages/search.html'

    def get_context_data(self, **kwargs):
        text_to_search = self.kwargs['text']
        odas_list = [oda for oda in ODA.objects.filter(name__contains=text_to_search, temporal=False)
                     if oda.subject.ambit.is_published]
        tags = Tag.objects.filter(name__contains=text_to_search)

        for tag in tags:
            odas = tag.odas.all()
            for oda in tag.odas.all():
                if oda not in odas_list and not oda.temporal and oda.subject.ambit.is_published:
                    odas_list.append(oda)

        return {'odas_list': odas_list, 'text_to_search': text_to_search}

