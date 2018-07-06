from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import FormView

from alumnica_model.mixins import OnlyLearnerMixin
from alumnica_model.models import MicroODA


class MicroODAView(LoginRequiredMixin, OnlyLearnerMixin, FormView):
    login_url = "login_view"
    template_name = ""

    def dispatch(self, request, *args, **kwargs):
        super(MicroODAView,self).dispatch(*args, **kwargs)
        microoda = MicroODA.objects.get(pk=kwargs['pk'])
        moments_list = microoda.activities.order_by('default_position')
        return render(request, self.template_name, {'microoda': microoda, 'moments_list': moments_list})