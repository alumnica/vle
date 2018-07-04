import json
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, ViewSet

from alumnica_model.models import AuthUser, Learner, MicroODA
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
        score, answers, suggestions = self.review_evaluation(evaluation,
                                                      relationship_answers, multiple_option_answers,
                                                      multiple_answer_answers, numeric_answers,
                                                      pulldown_list_answers, user.profile)
        json_response = json.dumps(answers)
        return JsonResponse({'score': score, 'data': json_response, 'suggestions': suggestions})

    def review_evaluation(self, evaluation, relationship_answers, multiple_option_answers, multiple_answer_answers,
                          numeric_answers, pulldown_list_answers, learner):
        score = 0
        questions_status = []
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
                if correct_answer:
                    questions_status.append({'type': TYPE_RELATIONSHIP,
                                             'pk': question_instance.pk,
                                             'uoda_type':question_instance.microoda.name,
                                             'status': 'correct',
                                             'description': question_instance.success_description})
                else:
                    question_instance = RelationShipQuestion.objects.get(pk=int(question['question_pk']))
                    questions_status.append({'type': TYPE_RELATIONSHIP,
                                             'uoda_type':question_instance.microoda.name,
                                             'pk': question_instance.pk,
                                             'status': 'incorrect',
                                             'description': question_instance.fail_description})

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
                if correct_answer:
                    questions_status.append({'type': TYPE_PULL_DOWN_LIST,
                                             'uoda_type':question_instance.microoda.name,
                                             'pk': question_instance.pk,
                                             'status': 'correct',
                                             'description': question_instance.success_description})
                else:
                    question_instance = PullDownListQuestion.objects.get(pk=int(question['question_pk']))
                    questions_status.append({'type': TYPE_PULL_DOWN_LIST,
                                             'uoda_type':question_instance.microoda.name,
                                             'pk': question_instance.pk,
                                             'status': 'incorrect',
                                             'description': question_instance.fail_description})

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
                if correct_answer:
                    questions_status.append({'type': TYPE_MULTIPLE_OPTION,
                                             'uoda_type':question_instance.microoda.name,
                                             'pk': question_instance.pk,
                                             'status': 'correct',
                                             'description': question_instance.success_description})
                else:
                    question_instance = MultipleOptionQuestion.objects.get(pk=int(question['question_pk']))
                    questions_status.append({'type': TYPE_MULTIPLE_OPTION,
                                             'uoda_type':question_instance.microoda.name,
                                             'pk': question_instance.pk,
                                             'status': 'incorrect',
                                             'description': question_instance.fail_description})

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
                if correct_answer:
                    questions_status.append({'type': TYPE_MULTIPLE_ANSWER,
                                             'uoda_type':question_instance.microoda.name,
                                             'pk': question_instance.pk,
                                             'status': 'correct',
                                             'description': question_instance.success_description})
                else:
                    question_instance = MultipleAnswerQuestion.objects.get(pk=int(question['question_pk']))
                    questions_status.append({'type': TYPE_MULTIPLE_ANSWER,
                                             'uoda_type':question_instance.microoda.name,
                                             'pk': question_instance.pk,
                                             'status': 'incorrect',
                                             'description': question_instance.fail_description})

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
                if correct_answer:
                    questions_status.append({'type': TYPE_NUMERIC_ANSWER,
                                             'uoda_type':question_instance.microoda.name,
                                             'pk': question_instance.pk,
                                             'status': 'correct',
                                             'description': question_instance.success_description})
                else:
                    question_instance = NumericQuestion.objects.get(pk=int(question['question_pk']))
                    questions_status.append({'type': TYPE_NUMERIC_ANSWER,
                                             'uoda_type':question_instance.microoda.name,
                                             'pk': question_instance.pk,
                                             'status': 'incorrect',
                                             'description': question_instance.fail_description})

        evaluation_completed = False
        if score >= 7:
            self_oda_pk = question_instance.evaluation.oda.all()[0].pk
            odas_array = [tag.odas.filter(temporal=False) for tag in question_instance.evaluation.oda.all()[0].tags.all()]
            suggestions_dict = []

            for odas in odas_array:
                for oda in odas:
                    if oda.pk != self_oda_pk and oda.subject.ambit.is_published:
                        suggestions_dict.append({'oda': oda.name, 'image': oda.active_icon.file.url, 'pk': oda.pk})

            evaluation_completed = True
        else:
            suggestions = [question['uoda_type'] for question in questions_status
                           if question['status'] == 'incorrect']
            suggestions = set(suggestions)
            suggestions_dict = [{'uoda': uoda} for uoda in suggestions]

        if learner.evaluations_progresses.filter(evaluation=question_instance.evaluation).exists():
            progress = learner.evaluations_progresses.get(evaluation=question_instance.evaluation)
            if not progress.is_complete and evaluation_completed:
                # To do. Give more points or stars or something
                progress.is_complete = evaluation_completed
                progress.save()
        else:
            progress = LearnerEvaluationProgress.objects.create(evaluation=question_instance.evaluation,
                                                                is_complete=evaluation_completed)
            learner.evaluations_progresses.add(progress)

        return score, questions_status, suggestions_dict


class MicroodaViewSet(APIView):
    def get(self, request,*args, **kwargs):
        learner_pk = kwargs['learner']
        microoda_pk = kwargs['uODA']

        learner = Learner.objects.get(pk=learner_pk)
        microoda = MicroODA.objects.get(pk=microoda_pk)

        for activity in microoda.activities.all():
            progress = learner.activities_progresses.get(activity=activity)
            progress.is_complete = True
            progress.save()

        microodas_suggestion = [{'mODA_name': mODA.type.name} for mODA in microoda.oda.microodas.exclude(pk=microoda.pk)]


        return JsonResponse({'points': 10, 'suggestions': microodas_suggestion})

