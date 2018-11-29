import datetime
import random

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import FormView

from alumnica_model.mixins import OnlyLearnerMixin, LoginCounterMixin
from alumnica_model.models.content import Evaluation, ODA
from alumnica_model.models.questions import TYPE_RELATIONSHIP, TYPE_PULL_DOWN_LIST, TYPE_MULTIPLE_OPTION, \
    TYPE_MULTIPLE_ANSWER, TYPE_NUMERIC_ANSWER
from webapp.gamification import evaluation_completed_xp
from webapp.statement_builders import access_statement_with_parent


class EvaluationView(LoginRequiredMixin, OnlyLearnerMixin, LoginCounterMixin, FormView):
    """
    Random Evaluation questions view
    """
    login_url = 'login_view'
    template_name = 'webapp/pages/eval.html'
    evaluation = []

    def dispatch(self, request, *args, **kwargs):
        response = super(EvaluationView, self).dispatch(request, *args, **kwargs)
        if response.status_code == 200 and request.method == 'GET':
            evaluation = Evaluation.objects.get(pk=self.kwargs['pk'])
            timestamp = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc).isoformat()
            access_statement_with_parent(request=request,
                                         object_type='evaluation',
                                         object_name=evaluation.name,
                                         parent_type='oda',
                                         parent_name=evaluation.oda.all()[0].name,
                                         tags_array=evaluation.oda.all()[0].tags.all(),
                                         timestamp=timestamp)
        return response

    def get_context_data(self, **kwargs):
        self.evaluation = []
        self.get_evaluation(self.kwargs['pk'])
        learner = self.request.user.profile
        completed_uodas = 0
        evaluation = Evaluation.objects.get(pk=self.kwargs['pk'])
        progress, created = learner.evaluations_progresses.get_or_create(evaluation=evaluation)

        for uoda in evaluation.oda.first().microodas.all():
            if learner.activities_progresses.filter(
                    activity=uoda.activities.first()).exists() and learner.activities_progresses.get(
                activity=uoda.activities.first()).is_complete:
                completed_uodas += 1

        xp, equation = evaluation_completed_xp(login_counter=learner.login_progress.login_counter,
                                               completed_uodas=completed_uodas,
                                               completed_counter=(progress.evaluation_completed_counter+1))
        oda = ODA.objects.get(evaluation=Evaluation.objects.get(pk=self.kwargs['pk']))
        return {'evaluation': self.evaluation, 'oda': oda, 'xp': xp, 'equation': equation}

    def get_evaluation(self, pk):
        """
        Gets random questions
        :param pk: evaluation primary key
        """
        evaluation_instance = Evaluation.objects.get(pk=pk)
        micro_oda_array = list(evaluation_instance.oda.all()[0].microodas.all())
        random.shuffle(micro_oda_array)
        for microODA in micro_oda_array:
            microoda_questions = []
            microoda_questions.extend(evaluation_instance.relationship_questions.filter(microoda=microODA.type))
            microoda_questions.extend(evaluation_instance.multiple_option_questions.filter(microoda=microODA.type))
            microoda_questions.extend(evaluation_instance.multiple_answer_questions.filter(microoda=microODA.type))
            microoda_questions.extend(evaluation_instance.numeric_questions.filter(microoda=microODA.type))
            microoda_questions.extend(evaluation_instance.pull_down_list_questions.filter(microoda=microODA.type))

            random_questions = random.sample(microoda_questions, 2)

            for question in random_questions:
                if question.type == TYPE_RELATIONSHIP:
                    answers = question.answers.split('|')
                    random.shuffle(answers)
                    self.evaluation.append([question, answers])
                elif question.type == TYPE_PULL_DOWN_LIST:
                    answers = question.answers.split('|')
                    questions = question.options.split('|')
                    random.shuffle(answers)
                    random.shuffle(questions)
                    self.evaluation.append([question, answers, questions])
                elif question.type == TYPE_MULTIPLE_OPTION:
                    answers = question.incorrect_answers.split('|')
                    answers.append(question.correct_answer)
                    random.shuffle(answers)
                    self.evaluation.append([question, answers])
                elif question.type == TYPE_MULTIPLE_ANSWER:
                    answers = question.incorrect_answers.split('|')
                    answers.extend(question.correct_answers.split('|'))
                    random.shuffle(answers)
                    self.evaluation.append([question, answers])
                elif question.type == TYPE_NUMERIC_ANSWER:
                    self.evaluation.append([question, 0])
