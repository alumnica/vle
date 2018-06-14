from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import FormView

from alumnica_model.models import Moment


class MomentView(LoginRequiredMixin, FormView):
    login_url = "login_view"
    template_name = "webapp/pages/momentos.html"

    def dispatch(self, request, *args, **kwargs):
        moment = Moment.objects.get(pk=kwargs['pk'])
        return render(request, self.template_name, {'moment': moment})