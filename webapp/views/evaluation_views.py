import random
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import FormView
from alumnica_model.models.content import Evaluation


class EvaluationView(LoginRequiredMixin, FormView):
    login_url = 'login_view'
    template_name = 'webapp/pages/test.html'
    evaluation = []

    def dispatch(self, request, *args, **kwargs):
        self.evaluation = []
        self.get_evaluation(kwargs['pk'])
        return render(request, self.template_name, {'evaluation': self.evaluation})

    def get_evaluation(self, pk):
        evaluation_instance = Evaluation.objects.get(pk=pk)
        microoda_questions = []
        for microODA in evaluation_instance.oda.all()[0].microodas.all():
            microoda_questions.extend(evaluation_instance.relationship_questions.all())
            microoda_questions.extend(evaluation_instance.multiple_option_questions.all())
            microoda_questions.extend(evaluation_instance.multiple_answer_questions.all())
            microoda_questions.extend(evaluation_instance.numeric_questions.all())
            microoda_questions.extend(evaluation_instance.pull_down_list_questions.all())

            sample_questions = random.sample(microoda_questions, 2)
            self.evaluation.append([microODA.type.name, sample_questions])
