from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView


class AmbitGridView(LoginRequiredMixin, TemplateView):
    login_url = 'login_view'
    template_name = 'webapp/pages/ambitos-grid.html'