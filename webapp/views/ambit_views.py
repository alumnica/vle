import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import FormView, TemplateView

from alumnica_model.mixins import OnlyLearnerMixin, LoginCounterMixin
from alumnica_model.models import Ambit


class AmbitGridView(LoginRequiredMixin, OnlyLearnerMixin, LoginCounterMixin, FormView):
    """
    Published Ámbitos Grid view
    """
    login_url = 'login_view'
    template_name = 'webapp/pages/ambitos-grid.html'

    def dispatch(self, request, *args, **kwargs):
        response = super(AmbitGridView, self).dispatch(request, *args, **kwargs)
        if response.status_code == 200 and request.method == 'GET':
            timestamp = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc).isoformat()
        return response

    def get_context_data(self, **kwargs):
        ambits_list = Ambit.objects.all().filter(is_published=True).order_by('position')
        return {'ambits_list': ambits_list}


class TestView(TemplateView):
    template_name = 'webapp/pages/test.html'
