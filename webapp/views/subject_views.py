from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import DetailView
from django.views.generic.base import View

from alumnica_model.models import SubjectModel


class SubjectView(LoginRequiredMixin, View):
    login_url = 'login_view'
    template_name = 'webapp/pages/test.html'
    model = SubjectModel

    def dispatch(self, request, *args, **kwargs):
        subject = SubjectModel.objects.get(pk=self.kwargs['pk'])
        return render(request, self.template_name, {'subject': subject})