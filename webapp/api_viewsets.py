import datetime
import json

from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from alumnica_model.models import AuthUser, Learner, MicroODA, Moment
from alumnica_model.models.progress import LearnerEvaluationProgress, EXPERIENCE_POINTS_CONSTANTS
from alumnica_model.models.questions import *
from webapp.serializers import *
from webapp.statement_builders import task_completed, task_experience_received, avatar_statement, \
    answered_question_statement, h5p_task_completed


class EvaluationViewSet(ModelViewSet):
    """
    Review evaluation ViewSet
    """
    serializer_class = EvaluationSerializer
    queryset = Evaluation.objects.all()

    def list(self, request, *args, **kwargs):
        """
        Obtains original Evaluation questions and user answers
        :param request: Contains all evaluation data
        :return: score, answer statuses and suggestions
        """
        duration = request.GET['duration']
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
                                                             pulldown_list_answers, user.profile, duration)
        json_response = json.dumps(answers)
        return JsonResponse({'score': score, 'data': json_response, 'suggestions': suggestions})

    def review_evaluation(self, evaluation, relationship_answers, multiple_option_answers, multiple_answer_answers,
                          numeric_answers, pulldown_list_answers, learner, duration):
        """
        Compares user answers with correct and incorrect answers stored in database
        :param evaluation: original answers order by randomly chosen question
        :param relationship_answers: Index answers to all relationship questions type, separated by pipes
        :param multiple_option_answers: Index answers to all multiple option questions type, separated by pipes
        :param multiple_answer_answers: Index answers to all multiple answer questions type, separated by pipes
        :param numeric_answers: Index answers to all numeric questions type, separated by pipes
        :param pulldown_list_answers: Index answers to all pull down questions type, separated by pipes
        :param learner: Current AuthUser Learner profile
        :param duration: Time spent by the user answering the evaluation
        :return: Score obtained, answers statuses and suggestions (ODAs or MicroODAs)
        """
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
                                             'uoda_type': question_instance.microoda.name,
                                             'status': 'correct',
                                             'description': question_instance.success_description})
                else:
                    question_instance = RelationShipQuestion.objects.get(pk=int(question['question_pk']))
                    questions_status.append({'type': TYPE_RELATIONSHIP,
                                             'uoda_type': question_instance.microoda.name,
                                             'pk': question_instance.pk,
                                             'status': 'incorrect',
                                             'description': question_instance.fail_description})

            elif question['question_type'] == TYPE_PULL_DOWN_LIST:
                local_score = 0
                for answer_data in pulldown_list_answers:
                    answer = answer_data.split(';')
                    if question['question_pk'] == answer[0]:
                        question_instance = PullDownListQuestion.objects.get(pk=int(answer[0]))
                        options_instance = question_instance.options.split('|')
                        answer_instance = question_instance.answers.split('|')

                        index = 0
                        for answer_element in answer[1:]:
                            answer_element_array = answer_element.split(',')
                            option_instance_index = options_instance.index(question['options'][index]['option'])

                            answer_expected = answer_instance[option_instance_index]
                            answer_obtained = question['answers'][int(answer_element_array[1])]['answer']

                            if answer_expected.strip() == answer_obtained.strip():
                                local_score += 1
                            index += 1
                        if local_score == len(answer_instance):
                            correct_answer = True
                            score += 1
                        break
                if correct_answer:
                    questions_status.append({'type': TYPE_PULL_DOWN_LIST,
                                             'uoda_type': question_instance.microoda.name,
                                             'pk': question_instance.pk,
                                             'status': 'correct',
                                             'description': question_instance.success_description})
                else:
                    question_instance = PullDownListQuestion.objects.get(pk=int(question['question_pk']))
                    questions_status.append({'type': TYPE_PULL_DOWN_LIST,
                                             'uoda_type': question_instance.microoda.name,
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
                                             'uoda_type': question_instance.microoda.name,
                                             'pk': question_instance.pk,
                                             'status': 'correct',
                                             'description': question_instance.success_description})
                else:
                    question_instance = MultipleOptionQuestion.objects.get(pk=int(question['question_pk']))
                    questions_status.append({'type': TYPE_MULTIPLE_OPTION,
                                             'uoda_type': question_instance.microoda.name,
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
                                             'uoda_type': question_instance.microoda.name,
                                             'pk': question_instance.pk,
                                             'status': 'correct',
                                             'description': question_instance.success_description})
                else:
                    question_instance = MultipleAnswerQuestion.objects.get(pk=int(question['question_pk']))
                    questions_status.append({'type': TYPE_MULTIPLE_ANSWER,
                                             'uoda_type': question_instance.microoda.name,
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
                                             'uoda_type': question_instance.microoda.name,
                                             'pk': question_instance.pk,
                                             'status': 'correct',
                                             'description': question_instance.success_description})
                else:
                    question_instance = NumericQuestion.objects.get(pk=int(question['question_pk']))
                    questions_status.append({'type': TYPE_NUMERIC_ANSWER,
                                             'uoda_type': question_instance.microoda.name,
                                             'pk': question_instance.pk,
                                             'status': 'incorrect',
                                             'description': question_instance.fail_description})

            timestamp = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc).isoformat()
            tags = question_instance.evaluation.oda.all()[0].microodas.get(type=question_instance.microoda).tags.all()
            answered_question_statement(user=learner.auth_user, question_instance=question_instance,
                                        success=correct_answer, timestamp=timestamp, tags_array=tags)

        evaluation_completed = False
        evaluation_instance = question_instance.evaluation
        if score >= 7:
            self_oda_pk = question_instance.evaluation.oda.all()[0].pk
            odas_array = [tag.odas.filter(temporal=False) for tag in
                          question_instance.evaluation.oda.all()[0].tags.all()]
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
            suggestions_dict = [{'uoda': uoda, 'pk': evaluation_instance.oda.all()[0].microodas.get(type=MicroODAType.objects.get(name=uoda)).activities.first().pk} for uoda in suggestions]

        if learner.evaluations_progresses.filter(evaluation=question_instance.evaluation).exists():
            progress = learner.evaluations_progresses.get(evaluation=question_instance.evaluation)
            if not progress.is_complete and evaluation_completed:
                progress.is_complete = evaluation_completed
                timestamp = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc).isoformat()
                task_experience_received(user=learner.auth_user,
                                         object_type='evaluation',
                                         object_name=evaluation_instance.name,
                                         parent_type='oda',
                                         parent_name=evaluation_instance.oda.all()[0].name,
                                         tags_array=evaluation_instance.oda.all()[0].tags.all(),
                                         timestamp=timestamp,
                                         gained_xp=EXPERIENCE_POINTS_CONSTANTS['evaluation_completed'])
            progress.evaluation_completed_counter += 1
            progress.save_progress()
        else:
            progress = LearnerEvaluationProgress.objects.create(evaluation=question_instance.evaluation,
                                                                is_complete=evaluation_completed)
            learner.evaluations_progresses.add(progress)
            progress.evaluation_completed_counter += 1
            progress.save_progress()

        timestamp = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc).isoformat()
        task_completed(learner.auth_user,
                       'evaluation',
                       evaluation_instance.name,
                       'oda', evaluation_instance.oda.all()[0].name,
                       tags_array=evaluation_instance.oda.all()[0].tags.all(),
                       timestamp=timestamp,
                       score=score,
                       duration=duration)

        return score, questions_status, suggestions_dict


class MicroodaViewSet(APIView):
    """
    Set Activities completed status by MicroODA
    """
    def get(self, request, *args, **kwargs):
        learner_pk = kwargs['learner']
        microoda_pk = kwargs['uODA']
        duration = kwargs['duration']

        learner = Learner.objects.get(pk=learner_pk)
        microoda = MicroODA.objects.get(pk=microoda_pk)

        for activity in microoda.activities.all():
            progress = learner.activities_progresses.get(activity=activity)
            progress.activity_completed_counter += 1
            progress.is_complete = True
            progress.save_progress()

            if progress.activity_completed_counter == 1:
                timestamp = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc).isoformat()
                task_experience_received(user=learner.auth_user,
                                         object_type='uoda',
                                         object_name=microoda.name,
                                         parent_type='oda',
                                         parent_name=microoda.oda.name,
                                         tags_array=microoda.tags.all(),
                                         timestamp=timestamp,
                                         gained_xp=EXPERIENCE_POINTS_CONSTANTS['uODA_completed'])

        timestamp = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc).isoformat()
        task_completed(user=learner.auth_user,
                       object_type='uoda',
                       object_name=microoda.name,
                       parent_type='oda', parent_name=microoda.oda.name,
                       tags_array=microoda.tags.all(),
                       timestamp=timestamp,
                       duration=duration)

        microodas_suggestion = [{'mODA_name': mODA.type.name} for mODA in
                                microoda.oda.microodas.exclude(pk=microoda.pk)]

        return JsonResponse({'points': 10, 'suggestions': microodas_suggestion})


class ChangeUserAvatar(APIView):
    """
    Learner changed avatar selection saver
    """
    def get(self, request, *args, **kwargs):
        learner_pk = request.GET['pk']
        avatar_id = request.GET['avatar']
        learner = AuthUser.objects.get(pk=learner_pk)

        learner.profile.avatar = avatar_id
        learner.profile.save()

        timestamp = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc).isoformat()
        avatar_statement(user=learner, avatar=avatar_id, timestamp=timestamp)
        return JsonResponse({'ok': 'ok'})


class SaveExtraProfileInfo(APIView):
    """
    Edit Learner extra info
    """
    def get(self, request):
        learner_pk = request.GET['learner']
        learner = AuthUser.objects.get(pk=learner_pk)
        return JsonResponse({'favourite_subject': learner.profile.favourite_subject,
                             'working_time': learner.profile.working_time,
                             'university_studies': learner.profile.university_studies})

    def post(self, request):
        learner_pk = request.POST['learner']
        favourite_subject = request.POST['favourite_subject']
        working_time = request.POST['working_time']
        university_studies = request.POST['university_studies']

        learner = AuthUser.objects.get(pk=learner_pk)

        learner.profile.favourite_subject = favourite_subject
        learner.profile.working_time = working_time
        learner.profile.university_studies = university_studies

        learner.profile.save()
        return JsonResponse({'ok': 'ok'})


class H5PToXapi(APIView):
    def post(self, request, subContentId):
        pass


class H5PFinished(APIView):
    def post(self, request, user, momento):
        momento_instance = Moment.objects.get(pk=momento)
        auth_user = AuthUser.objects.get(pk=user)
        score = int(request.POST.get('score'))
        max_score = int(request.POST.get('maxScore'))
        timestamp = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc).isoformat()
        h5p_task_completed(user=auth_user, object_type='Momento', object_name=momento_instance.name,
                       parent_type="uoda", parent_name=momento_instance.microoda.name, tags_array=momento_instance.tags.all(),
                       timestamp=timestamp, score=score, max_score=max_score)
        return JsonResponse({'ok': 'ok'})



