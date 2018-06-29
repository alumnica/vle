import json
import random
from collections import namedtuple

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render_to_response
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ViewSet

from alumnica_model.models import AuthUser
from alumnica_model.models.progress import LearnerEvaluationProgress
from alumnica_model.models.questions import *
from webapp.serializers import *


class EvaluationViewSet(ModelViewSet):
    serializer_class = EvaluationSerializer
    queryset = Evaluation.objects.all()

    def list(self, request, *args, **kwargs):
        evaluation_data = request.GET['evaluation']
        evaluation = json.loads(evaluation_data)
        relationship_answers = request.GET['relationship_answers'].split('|')
        multiple_option_answers = request.GET['multiple_option_answers'].split('|')
        multiple_answer_answers = request.GET['multiple_answer_answers'].split('|')
        numeric_answers = request.GET['numeric_answer_answers'].split('|')
        pulldown_list_answers = request.GET['pulldown_list_answers'].split('|')
        user_pk = request.GET['pk']
        user = AuthUser.objects.get(pk=user_pk)
        score, wrong_answers = self.review_evaluation(evaluation,
                                                      relationship_answers, multiple_option_answers,
                                                      multiple_answer_answers, numeric_answers,
                                                      pulldown_list_answers, user.profile)
        json_response = json.dumps(wrong_answers)
        return JsonResponse({'score':score,'data': json_response})

    def review_evaluation(self, evaluation, relationship_answers, multiple_option_answers, multiple_answer_answers,
                          numeric_answers, pulldown_list_answers, learner):
        score = 0
        wrong_answers = []
        question_instance = None

        for question in evaluation:
            correct_answer = False
            if question['question_type'] == TYPE_RELATIONSHIP:
                local_score = 0
                for answer_data in relationship_answers:
                    answer = answer_data.split(';')
                    if question['question_pk'] == answer[0]:
                        question_instance = RelationShipQuestion.objects.get(pk=int(answer[0]))
                        answer_instance = question_instance.answers.split('|')
                        for answer_element in answer[1:]:
                            answer_element_array = answer_element.split(',')
                            answer_expected = answer_instance[int(answer_element_array[0])]
                            answer_obtained = question['answers'][int(answer_element_array[1])]['answer']

                            if answer_expected.strip() == answer_obtained.strip():
                                local_score += 1
                        if local_score == len(answer_instance):
                            correct_answer = True
                            score += 1
                        break
                if not correct_answer:
                    question_instance = RelationShipQuestion.objects.get(pk=int(question['question_pk']))
                    wrong_answers.append({'type': TYPE_RELATIONSHIP, 'pk': question_instance.pk})

            elif question['question_type'] == TYPE_PULL_DOWN_LIST:
                local_score = 0
                for answer_data in pulldown_list_answers:
                    answer = answer_data.split(';')
                    if question['question_pk'] == answer[0]:
                        question_instance = PullDownListQuestion.objects.get(pk=int(answer[0]))
                        answer_instance = question_instance.answers.split('|')
                        for answer_element in answer[1:]:
                            answer_element_array = answer_element.split(',')
                            answer_expected = answer_instance[int(answer_element_array[0])]
                            answer_obtained = question['answers'][int(answer_element_array[1])]['answer']

                            if answer_expected.strip() == answer_obtained.strip():
                                local_score += 1
                        if local_score == len(answer_instance):
                            correct_answer = True
                            score += 1
                        break
                if not correct_answer:
                    question_instance = PullDownListQuestion.objects.get(pk=int(question['question_pk']))
                    wrong_answers.append({'type': TYPE_PULL_DOWN_LIST, 'pk': question_instance.pk})

            elif question['question_type'] == TYPE_MULTIPLE_OPTION:
                for answer_data in multiple_option_answers:
                    answer = answer_data.split(';')
                    if question['question_pk'] == answer[0]:
                        question_instance = MultipleOptionQuestion.objects.get(pk=int(answer[0]))
                        answer_expected = question_instance.correct_answer
                        answer_obtained = question['answers'][int(answer[1])]['answer']

                        if answer_expected.strip() == answer_obtained.strip():
                            correct_answer = True
                            score += 1
                        break
                if not correct_answer:
                    question_instance = MultipleOptionQuestion.objects.get(pk=int(question['question_pk']))
                    wrong_answers.append({'type': TYPE_MULTIPLE_OPTION, 'pk': question_instance.pk})

            elif question['question_type'] == TYPE_MULTIPLE_ANSWER:
                local_score = 0
                for answer_data in multiple_answer_answers:
                    answer = answer_data.split(';')
                    if question['question_pk'] == answer[0]:
                        question_instance = MultipleAnswerQuestion.objects.get(pk=int(answer[0]))
                        answer_element_array = answer[1:]
                        answer_instance = question_instance.correct_answers.split('|')
                        for index_obtained in answer_element_array:
                            answer_obtained = question['answers'][int(index_obtained)]['answer']
                            if answer_obtained in answer_instance:
                                local_score += 1
                        if local_score == len(answer_instance):
                            score += 1
                            correct_answer = True
                        break
                if not correct_answer:
                    question_instance = MultipleAnswerQuestion.objects.get(pk=int(question['question_pk']))
                    wrong_answers.append({'type': TYPE_MULTIPLE_ANSWER, 'pk': question_instance.pk})

            elif question['question_type'] == TYPE_NUMERIC_ANSWER:
                for answer_data in numeric_answers:
                    answer = answer_data.split(';')
                    if question['question_pk'] == answer[0]:
                        question_instance = NumericQuestion.objects.get(pk=int(answer[0]))
                        answer_obtained = int(answer[1])
                        if question_instance.min_limit <= answer_obtained <= question_instance.max_limit:
                            score += 1
                            correct_answer = True
                        break
                if not correct_answer:
                    question_instance = NumericQuestion.objects.get(pk=int(question['question_pk']))
                    wrong_answers.append({'type': TYPE_NUMERIC_ANSWER, 'pk': question_instance.pk})

        progress = None
        evaluation_completed = False
        if score >= 7:
            evaluation_completed = True
        if learner.evaluations_progresses.filter(pk=question_instance.evaluation.pk).exists():
            progress = learner.evaluations_progresses.get(pk=question_instance.evaluation.pk)
            if not progress.is_complete and evaluation_completed:
                #To do. Give more points or stars or something
                progress.is_complete = evaluation_completed
        else:
            progress= LearnerEvaluationProgress.objects.create(evaluation=question_instance.evaluation, is_complete=evaluation_completed)
            learner.evaluations_progresses.add(progress)

        return score, wrong_answers