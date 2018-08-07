import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import FormView, TemplateView

from alumnica_model.mixins import OnlyLearnerMixin
from alumnica_model.models import Ambit
from webapp.statement_builders import access_statement


class AmbitGridView(LoginRequiredMixin, OnlyLearnerMixin, FormView):
    login_url = 'login_view'
    template_name = 'webapp/pages/ambitos-grid.html'

    def dispatch(self, request, *args, **kwargs):
        if request.method == 'GET':
            timestamp = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc).isoformat()
            access_statement(request, 'Ambitos Grid', timestamp)
        return super(AmbitGridView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ambits_list= Ambit.objects.all().filter(is_published=True).order_by('position')
        return {'ambits_list': ambits_list}


class TestView(TemplateView):
    template_name = 'webapp/pages/test.html'