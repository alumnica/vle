from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import RedirectView, FormView

from alumnica_model.mixins import OnlyLearnerMixin
from alumnica_model.models import ODA, Tag


# class SearchRedirectView(LoginRequiredMixin, OnlyLearnerMixin, FormView):
#     login_url = 'login_view'
#     template_name = 'webapp/partials/nav-logged-in.html'
#
#     def dispatch(self, request, *args, **kwargs):
#         return super(SearchRedirectView, self).dispatch(request, *args, **kwargs)
#
#     def form_valid(self, form):
#         text = self.request.POST.get('searcher')
#         return redirect(to='search_view', text=text)


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

