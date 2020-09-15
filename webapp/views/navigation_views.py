import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import FormView

from alumnica_model.mixins import OnlyLearnerMixin, LoginCounterMixin
from alumnica_model.models import ODA, Tag



class RecentActivitiesView(LoginRequiredMixin, OnlyLearnerMixin, FormView):
    """
    ODAs objects with at least one MicroODA visualized view
    """
    login_url = 'login_view'
    template_name = 'webapp/pages/recent.html'

    def get_context_data(self, **kwargs):
        odas_list = []

        for activity_progress in self.request.user.profile.activities_progresses.all():
            try :
                if activity_progress.activity.microoda.oda not in odas_list:
                    odas_list.append(activity_progress.activity.microoda.oda)
            except AttributeError:
                continue

        return {'odas_list': odas_list}


class SearchView(LoginRequiredMixin, OnlyLearnerMixin, LoginCounterMixin, FormView):
    """
    Searches string in Tags and ODAs names
    """
    login_url = 'login_view'
    template_name = 'webapp/pages/search.html'

    def get_context_data(self, **kwargs):
        text_to_search = self.kwargs['text']
        odas_list = [oda for oda in ODA.objects.filter(name__icontains=text_to_search, temporal=False)
                     if oda.subject.ambit.is_published]
        tags = Tag.objects.filter(name__icontains=text_to_search)

        for tag in tags:
            for oda in tag.odas.all():
                if oda not in odas_list and oda.subject is not None:
                    if oda.subject.ambit is not None and oda.subject.ambit.is_published:
                        odas_list.append(oda)

        timestamp = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc).isoformat()
        return {'odas_list': odas_list, 'text_to_search': text_to_search}


def error404(request, exception):
    """
    Handles custom 404 error page
    """
    return render(request, 'webapp/pages/404.html', status=404)

def error500(request):
    """
    Handles custom 500 error page
    """
    return render(request, 'webapp/pages/404.html', status=500)

