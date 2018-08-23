import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render_to_response, render
from django.template import RequestContext
from django.views.generic import FormView, TemplateView

from alumnica_model.mixins import OnlyLearnerMixin
from alumnica_model.models import ODA, Tag
from webapp.statement_builders import search_statement


class RecentActivitiesView(LoginRequiredMixin, OnlyLearnerMixin, FormView):
    """
    ODAs objects with at least one MicroODA visualized view
    """
    login_url = 'login_view'
    template_name = 'webapp/pages/recent.html'

    def get_context_data(self, **kwargs):
        odas_list = []

        for activity_progress in self.request.user.profile.activities_progresses.all():
            if activity_progress.activity.microoda.oda not in odas_list:
                odas_list.append(activity_progress.activity.microoda.oda)

        return {'odas_list': odas_list}


class SearchView(LoginRequiredMixin, OnlyLearnerMixin, FormView):
    """
    Searches string in Tags and ODAs names
    """
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

        timestamp = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc).isoformat()
        search_statement(user=self.request.user, string_searched=text_to_search, timestamp=timestamp)

        return {'odas_list': odas_list, 'text_to_search': text_to_search}


def Error404(request):
    return render(request, 'webapp/pages/404.html', status=404)
