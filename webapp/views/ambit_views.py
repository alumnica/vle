from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from alumnica_model.models import AmbitModel


class AmbitGridView(LoginRequiredMixin, ListView):
    login_url = 'login_view'
    template_name = 'webapp/pages/ambitos-grid.html'
    queryset = AmbitModel.objects.all()
    context_object_name = 'ambits_list'