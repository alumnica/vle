import random
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import FormView
from alumnica_model.models.content import Evaluation
from alumnica_model.models.questions import TYPE_RELATIONSHIP, TYPE_PULL_DOWN_LIST, TYPE_MULTIPLE_OPTION, \
    TYPE_MULTIPLE_ANSWER
from webapp.forms.evaluation_forms import EvaluationForm


class EvaluationView(LoginRequiredMixin, FormView):
    login_url = 'login_view'
    template_name = 'webapp/pages/test.html'
    evaluation = []
    form_class = EvaluationForm

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

            random_questions = random.sample(microoda_questions, 2)

            for question in random_questions:
                if question.type == TYPE_RELATIONSHIP or question.type == TYPE_PULL_DOWN_LIST:
                    self.evaluation.append([microODA.type.name, question, random.shuffle(question.answers)])
                elif question.type == TYPE_MULTIPLE_OPTION:
                    answers = question.incorrect_answers
                    answers.append(question.correct_answer)
                    self.evaluation.append([microODA.type.name, question, random.shuffle(answers)])
                elif question.type == TYPE_MULTIPLE_ANSWER:
                    answers = question.incorrect_answers
                    answers.append(question.correct_answers)
                    self.evaluation.append([microODA.type.name, question, random.shuffle(answers)])

    def form_valid(self, form):
        relationship_answers = self.request.POST.get('')
        multiple_option_answers = self.request.POST.get('')
        multiple_answer_answers = self.request.POST.get('')
        numeric_answers = self.request.POST.get('')
        pulldown_list_answers = self.request.POST.get('')

        score, microodas = form.review_evaluation(self.evaluation,
                                                  relationship_answers, multiple_option_answers,
                                                  multiple_answer_answers, numeric_answers,
                                                  pulldown_list_answers, self.request.user)


