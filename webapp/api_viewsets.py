import random
from collections import namedtuple

from django.shortcuts import render_to_response
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ViewSet

from alumnica_model.models.progress import LearnerEvaluationProgress
from alumnica_model.models.questions import *
from webapp.serializers import *


class EvaluationViewSet(ModelViewSet):
    serializer_class = EvaluationSerializer
    queryset = Evaluation.objects.all()
    evaluation = None

    def list(self, request, *args, **kwargs):
        eva = request.data
        evaluation = request.GET.getlist('evaluation[]',[])
        relationship_answers = self.request.GET('')
        multiple_option_answers = self.request.GET('')
        multiple_answer_answers = self.request.GET('')
        numeric_answers = self.request.data.GET('')
        pulldown_list_answers = self.request.data.GET('')

        score, wrong_answers = self.review_evaluation(self.evaluation,
                                                      relationship_answers, multiple_option_answers,
                                                      multiple_answer_answers, numeric_answers,
                                                      pulldown_list_answers, self.request.user.profile)
        return Response({'response':status.HTTP_200_OK, 'score': score, 'wrong_answers':wrong_answers})

    def review_evaluation(self, evaluation, relationship_answers, multiple_option_answers, multiple_answer_answers,
                          numeric_answers, pulldown_list_answers, learner):
        score = 0
        wrong_answers = []

        answers = relationship_answers.split('|')
        for answer_text in answers:
            local_score = 0
            answer = answer_text.split(';')
            relationship_question = [question_instance
                                     for question_instance in evaluation
                                     if question_instance[0].type == TYPE_RELATIONSHIP
                                     and question_instance[0].pk == int(answer[0])]
            if isinstance(relationship_question[0], RelationShipQuestion):
                answer_instance = relationship_question[1].answers.split('|')
                for answer_element in answer[1:]:
                    answer_element_array = answer_element.split(',')
                    answer_expected = answer_instance[int(answer_element_array[0])]
                    answer_obtained = relationship_question[1][int(answer_element_array[1])]

                    if answer_expected.strip() == answer_obtained.strip():
                        local_score += 1
                if local_score == len(answer_instance):
                    score += 1
                else:
                    wrong_answers.append([TYPE_RELATIONSHIP, relationship_question[0].pk])

        answers = multiple_option_answers.split('|')
        for answer_text in answers:
            answer = answer_text.split(';')
            multiple_option_question = [question_instance
                                        for question_instance in evaluation
                                        if question_instance[0].type == TYPE_MULTIPLE_OPTION
                                        and question_instance[0].pk == int(answer[0])]
            if isinstance(multiple_option_question[0], MultipleOptionQuestion):
                answer_expected = multiple_option_question[0].correct_answer
                answer_obtained = multiple_option_question[1][int(answer[1])]

                if answer_expected.strip() == answer_obtained.strip():
                    score += 1
                else:
                    wrong_answers.append([TYPE_MULTIPLE_OPTION, multiple_option_question[0].pk])

        answers = multiple_answer_answers.split('|')
        for answer_text in answers:
            local_score = 0
            answer = answer_text.split(';')
            multiple_answer_question = [question_instance
                                        for question_instance in evaluation
                                        if question_instance[0].type == TYPE_MULTIPLE_ANSWER
                                        and question_instance[0].pk == int(answer[0])]
            if isinstance(multiple_answer_question[0], MultipleAnswerQuestion):
                answer_instance = multiple_answer_question[0].correct_answers.split('|')
                answer_element_array = answer[1:]
                for index_obtained in answer_element_array:
                    answer_obtained = multiple_answer_question[1][int(index_obtained)]
                    if answer_obtained in answer_instance:
                        local_score += 1
                if local_score == len(answer_instance):
                    score += 1
                else:
                    wrong_answers.append([TYPE_MULTIPLE_ANSWER, multiple_answer_question[0].pk])

        answers = numeric_answers.split('|')
        for answer_text in answers:
            answer = answer_text.split(';')
            numeric_answer_question = [question_instance
                                       for question_instance in evaluation
                                       if question_instance[0].type == TYPE_NUMERIC_ANSWER
                                       and question_instance[0].pk == int(answer[0])]
            if isinstance(numeric_answer_question[0], NumericQuestion):
                answer_obtained = int(answer[1])

                if numeric_answer_question[0].min_limit <= answer_obtained <= numeric_answer_question[0].max_limit:
                    score += 1
                else:
                    wrong_answers.append([TYPE_NUMERIC_ANSWER, numeric_answer_question[0].pk])

        answers = pulldown_list_answers.split('|')
        for answer_text in answers:
            local_score = 0
            answer = answer_text.split(';')
            pulldown_list_question = [question_instance
                                      for question_instance in evaluation
                                      if question_instance[0].type == TYPE_PULL_DOWN_LIST
                                      and question_instance[0].pk == int(answer[0])]
            if isinstance(pulldown_list_question[0], PullDownListQuestion):
                answer_instance = pulldown_list_question[1].answers.split('|')
                for answer_element in answer[1:]:
                    answer_element_array = answer_element.split(',')
                    answer_expected = answer_instance[int(answer_element_array[0])]
                    answer_obtained = pulldown_list_question[1][int(answer_element_array[1])]

                    if answer_expected.strip() == answer_obtained.strip():
                        local_score += 1
                if local_score == len(answer_instance):
                    score += 1
                else:
                    wrong_answers.append([TYPE_PULL_DOWN_LIST, pulldown_list_question[0].pk])

        progress, created = LearnerEvaluationProgress.objects.get_or_create(learner=learner,
                                                                            evaluation=evaluation[0][0].evaluation)

        if score >= 8:
            progress.is_complete = True
            progress.save()

        return score, wrong_answers