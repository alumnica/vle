import random

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import FormView

from alumnica_model.models.content import Evaluation


class EvaluationView(LoginRequiredMixin, FormView):
    login_url = 'login_view'
    template_name = ''
    evaluation = []

    def get_context_data(self, **kwargs):
        context = super(EvaluationView, self).get_context_data(**kwargs)
        self.get_evaluation(kwargs['pk'])
        context.update({'evaluation': self.evaluation})
        return context

    def get_evaluation(self, pk):
        evaluation_instance = Evaluation.objects.get(pk=pk)
        microoda_questions = []
        for microODA in evaluation_instance.oda:
            microoda_questions.extend(evaluation_instance.relationship_questions)
            microoda_questions.extend(evaluation_instance.multiple_option_questions)
            microoda_questions.extend(evaluation_instance.multiple_answer_questions)
            microoda_questions.extend(evaluation_instance.numeric_questions)
            microoda_questions.extend(evaluation_instance.pull_down_list_questions)

            sample_questions = random.sample(microoda_questions, 2)
            self.evaluation.append([microODA.type.name, sample_questions])
