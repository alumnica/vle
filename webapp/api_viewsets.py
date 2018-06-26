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
    evaluation = []

    def list(self, request, *args, **kwargs):
        evaluation_to_send = namedtuple('evaluation_to_send',
                                ('relationship', 'multiple_option', 'multiple_answer', 'numeric', 'pulldown_list'))
        evaluation_to_send.relationship = []
        evaluation_to_send.multiple_option = []
        evaluation_to_send.multiple_answer = []
        evaluation_to_send.numeric = []
        evaluation_to_send.pulldown_list = []

        pk = request.GET['pk']
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
                if question.type == TYPE_RELATIONSHIP:
                    self.evaluation.append([question, random.shuffle(question.answers.split(','))])
                    question_serializer = RelationShipQuestionModelSerializer(question)
                    data = RelationShip(relationship=question_serializer,
                                        shuffle_answers=random.shuffle(question.answers.split(',')))
                    #data.relationship = question_serializer
                    #data.shuffle_answers = random.shuffle(question.answers.split(','))
                    evaluation_to_send.relationship.append(RelationShipSerializer(data))

                elif question.type == TYPE_PULL_DOWN_LIST:
                    self.evaluation.append([question, random.shuffle(question.answers.split(','))])
                    question_serializer = PullDownListQuestionModelSerializer(question)
                    data = PullDownList(pulldown_list=question_serializer,
                                        shuffle_answers=random.shuffle(question.answers.split(',')))
                    #data = namedtuple('data', ('shuffle_answers', 'pulldown_list'))
                    #data.pulldown_list = question_serializer
                    #data.shuffle_answers = random.shuffle(question.answers.split(','))
                    evaluation_to_send.pulldown_list.append(PullDownListSerializer(data))

                elif question.type == TYPE_MULTIPLE_OPTION:
                    answers = question.incorrect_answers.split(',')
                    answers.append(question.correct_answer)
                    self.evaluation.append([question, random.shuffle(answers)])
                    question_serializer = MultipleOptionQuestionModelSerializer(question)
                    data = MultipleOption(multiple_option=question_serializer,
                                        shuffle_answers=random.shuffle(answers))
                    #data = namedtuple('data', ('shuffle_answers', 'multiple_option'))
                    #data.multiple_option = question_serializer
                    #data.shuffle_answers = random.shuffle(answers)
                    evaluation_to_send.multiple_option.append(MultipleOptionSerializer(data))

                elif question.type == TYPE_MULTIPLE_ANSWER:
                    answers = question.incorrect_answers.split(',')
                    answers.append(question.correct_answers.split(','))
                    self.evaluation.append([question, random.shuffle(answers)])
                    question_serializer = MultipleAnswerQuestionModelSerializer(question)
                    data = MultipleAnswer(multiple_answer=question_serializer,
                                          shuffle_answers=random.shuffle(answers))
                    #data = namedtuple('data', ('shuffle_answers', 'multiple_answer'))
                    #data.multiple_answer = question_serializer
                    #data.shuffle_answers = random.shuffle(answers)
                    evaluation_to_send.multiple_answer.append(MultipleAnswerSerializer(data))

                elif question.type == TYPE_NUMERIC_ANSWER:
                    self.evaluation.append([question, question.min_limit])
                    question_serializer = NumericQuestionModelSerializer(question)
                    data = NumericAnswer(pk=question.pk,
                                          shuffle_answers=question.min_limit)
                    #data = namedtuple('data', ('shuffle_answers', 'numeric'))
                    #data.numeric = question_serializer
                    #data.shuffle_answers = question.min_limit
                    seriali = NumericAnswerSerializer(data)
                    evaluation_to_send.numeric.append(NumericAnswerSerializer(data))

        serializer = self.get_serializer(evaluation_to_send)
        return Response({'status': status.HTTP_200_OK, 'data': serializer.data}, template_name='webapp/pages/test.html')

    def get_score(self):
        relationship_answers = self.request.data.get('')
        multiple_option_answers = self.request.data.get('')
        multiple_answer_answers = self.request.data.get('')
        numeric_answers = self.request.data.get('')
        pulldown_list_answers = self.request.data.get('')

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