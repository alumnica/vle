import datetime
import json

from django.http import JsonResponse
from django.utils import timezone
from django.utils.dateparse import parse_date
from rest_framework.views import APIView

from alumnica_model.models import AuthUser, Learner, MicroODA, Moment, MicroODACompletedNotification, \
    EvaluationCompletedNotification, AchievementNotification, LevelUpNotification, AvatarEvolutionNotification, \
    AvatarAchievement, LearnerAvatarAchievement
from alumnica_model.models.notifications import AvatarAchievementNotification, LevelAchievementNotification, \
    TestAchievementNotification
from alumnica_model.models.questions import *
from alumnica_model.models.users import LearnerLevels, GENDER_TYPES
from webapp.gamification import uoda_completed_xp, evaluation_completed_xp, get_learner_level
from webapp.serializers import *
from webapp.statement_builders import task_completed, task_experience_received, avatar_statement, \
    answered_question_statement, h5p_task_completed


class EvaluationViewSet(APIView):
    """
    Review evaluation ViewSet
    """
    serializer_class = EvaluationSerializer
    queryset = Evaluation.objects.all()

    def post(self, request):
        """
        Obtains original Evaluation questions and user answers
        :param request: Contains all evaluation data
        :return: score, answer statuses and suggestions
        """
        duration = request.POST['duration']
        evaluation_data = request.POST['evaluation']
        evaluation = json.loads(evaluation_data)
        relationship_answers = request.POST['relationship_answers'].split('|')
        multiple_option_answers = request.POST['multiple_option_answers'].split('|')
        multiple_answer_answers = request.POST['multiple_answer_answers'].split('|')
        numeric_answers = request.POST['numeric_answer_answers'].split('|')
        pulldown_list_answers = request.POST['pulldown_list_answers'].split('|')
        user_pk = request.POST['pk']
        user = AuthUser.objects.get(pk=user_pk)
        score, answers, suggestions, equation, xp = self.review_evaluation(evaluation,
                                                                       relationship_answers, multiple_option_answers,
                                                                       multiple_answer_answers, numeric_answers,
                                                                       pulldown_list_answers, user.profile, duration)
        json_response = json.dumps(answers)
        return JsonResponse({'score': score, 'data': json_response, 'suggestions': suggestions, 'equation': equation, 'xp': xp})

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
                        answer_obtained = float(answer[1])
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
            suggestions_dict = [{'uoda': uoda, 'pk': evaluation_instance.oda.all()[0].microodas.get(
                type=MicroODAType.objects.get(name=uoda)).activities.first().pk} for uoda in suggestions]

        progress, created = learner.evaluations_progresses.get_or_create(evaluation=question_instance.evaluation)
        progress.is_complete = evaluation_completed
        progress.evaluation_completed_counter += 1
        progress.save()
        progress.check_general_badges_progress()
        learner.save()

        equation = None

        if evaluation_completed:
            completed_uodas = 0
            for uoda in evaluation_instance.oda.first().microodas.all():
                if learner.activities_progresses.filter(
                        activity=uoda.activities.first()).exists() and learner.activities_progresses.get(
                        activity=uoda.activities.first()).is_complete:
                    completed_uodas += 1
            xp, equation = evaluation_completed_xp(login_counter=learner.login_progress.login_counter,
                                                   completed_uodas=completed_uodas,
                                                   completed_counter=progress.evaluation_completed_counter)
            learner.assign_xp(xp)
            learner.save()

        timestamp = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc).isoformat()
        task_completed(learner.auth_user,
                       'evaluation',
                       evaluation_instance.name,
                       'oda', evaluation_instance.oda.all()[0].name,
                       tags_array=evaluation_instance.oda.all()[0].tags.all(),
                       timestamp=timestamp,
                       score=score,
                       duration=duration,
                       completion=evaluation_completed)

        EvaluationCompletedNotification.objects.create(learner=learner, evaluation=evaluation_instance, score=score)

        return score, questions_status, suggestions_dict, equation, xp


class MicroodaViewSet(APIView):
    """
    Set Activities completed status by MicroODA
    """

    def post(self, request, *args, **kwargs):
        learner_pk = kwargs['learner']
        microoda_pk = kwargs['uODA']
        duration = kwargs['duration']

        learner = Learner.objects.get(pk=learner_pk)
        microoda = MicroODA.objects.get(pk=microoda_pk)
        progress = None
        for activity in microoda.activities.all():
            progress = learner.activities_progresses.get(activity=activity)
            progress.activity_completed_counter += 1
            progress.is_complete = True
            progress.save()
        progress.check_progress()

        oda_sequence, created = learner.odas_sequence_progresses.get_or_create(oda=microoda.oda)
        if microoda.type.name not in oda_sequence.uoda_progress_order:
            oda_sequence.uoda_progress_order += ' {}'.format(microoda.type.name)
            oda_sequence.save()

        earned_xp, equation = uoda_completed_xp(login_counter=learner.login_progress.login_counter,
                                                oda_sequencing=oda_sequence.uoda_progress_order,
                                                learning_style=learner.learning_style.name,
                                                completed_counter=learner.activities_progresses.filter(
                                                    activity=microoda.activities.first()).first().activity_completed_counter)

        if earned_xp != 0:
            learner.assign_xp(earned_xp)
            timestamp = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc).isoformat()
            task_experience_received(user=learner.auth_user,
                                     object_type='uoda',
                                     object_name=microoda.name,
                                     parent_type='oda',
                                     parent_name=microoda.oda.name,
                                     tags_array=microoda.tags.all(),
                                     timestamp=timestamp,
                                     gained_xp=earned_xp)

        timestamp = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc).isoformat()
        task_completed(user=learner.auth_user,
                       object_type='uoda',
                       object_name=microoda.name,
                       parent_type='oda', parent_name=microoda.oda.name,
                       tags_array=microoda.tags.all(),
                       timestamp=timestamp,
                       duration=duration,
                       completion=True)

        MicroODACompletedNotification.objects.create(learner=learner, microoda=microoda, xp=earned_xp)

        return JsonResponse({'oda': microoda.oda.pk})


class ChangeUserAvatar(APIView):
    """
    Learner changed avatar selection saver
    """

    def get(self, request, *args, **kwargs):
        learner_pk = request.GET['learner']
        avatar_id = request.GET['avatar']
        learner = Learner.objects.get(pk=learner_pk)
        avatar_points = 0
        avatar = learner.avatar_progresses.get(avatar_name=avatar_id)
        if not avatar.active:
            for avatar_active in learner.avatar_progresses.filter(active=True):
                avatar_active.active = False
                avatar_active.save()
            avatar.active = True
            avatar.save()

        if avatar.points < 15000:
            avatar_points = avatar.points / 15000
        elif 15000 <= avatar.points < 50000:
            avatar_points = avatar.points / 50000
        elif avatar.points >= 50000:
            avatar_points = 1

        achievement = AvatarAchievement.objects.get(name='Selecciona un avatar diferente', counter=1)
        learner_achievement, created = LearnerAvatarAchievement.objects.get_or_create(learner=learner,
                                                                                      achievement=achievement)
        if created:
            AvatarAchievementNotification.objects.get_or_create(learner=learner, achievement=achievement)
            learner.assign_xp(achievement.xp)

        timestamp = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc).isoformat()
        avatar_statement(user=learner.auth_user, avatar=avatar_id, timestamp=timestamp)
        return JsonResponse({'avatar_points': avatar_points})


class SaveExtraProfileInfo(APIView):
    """
    Edit Learner extra info
    """

    def get(self, request):
        learner_pk = request.GET['learner']
        learner = Learner.objects.get(pk=learner_pk)
        return JsonResponse({'first_name': learner.auth_user.first_name,
                             'last_name': learner.auth_user.last_name,
                             'birth_date': learner.birth_date,
                             'gender': learner.gender,
                             'favourite_subject': learner.favourite_subject,
                             'working_time': learner.working_time,
                             'university_studies': learner.university_studies})

    def post(self, request):
        learner_pk = request.POST['learner']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        birth_date = request.POST['birth_date']
        gender = request.POST['gender']
        favourite_subject = request.POST['favourite_subject']
        working_time = request.POST['working_time']
        university_studies = request.POST['university_studies']

        learner = Learner.objects.get(pk=learner_pk)

        learner.auth_user.first_name = first_name
        learner.auth_user.last_name = last_name

        date = parse_date(birth_date)
        current_datetime = timezone.now().date()
        date_diff = current_datetime - date
        if (date.year + 160) < current_datetime.year or date_diff.days < 0:
            return JsonResponse({'status': 'false', 'message': 'La fecha no es válida'}, status=500)

        learner.birth_date = parse_date(birth_date)
        learner.gender = gender

        learner.favourite_subject = favourite_subject
        learner.working_time = working_time
        learner.university_studies = university_studies

        learner.save()
        return JsonResponse({'ok': 'ok'})


class H5PToXapi(APIView):
    def post(self, request, subContentId):
        pass


class H5PFinished(APIView):
    """
    Extracts score and sends h5p activity completion statement
    """

    def post(self, request, user, momento):
        momento_instance = Moment.objects.get(pk=momento)
        auth_user = AuthUser.objects.get(pk=user)
        score = int(request.POST.get('score'))
        max_score = int(request.POST.get('maxScore'))
        timestamp = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc).isoformat()
        h5p_task_completed(user=auth_user, object_type='Momento', object_name=momento_instance.name,
                           parent_type="uoda", parent_name=momento_instance.microoda.name,
                           tags_array=momento_instance.tags.all(),
                           timestamp=timestamp, score=score, max_score=max_score)
        return JsonResponse({'ok': 'ok'})


class NotificationsAPIView(APIView):
    def get(self, request):
        learner_pk = request.GET['learner']
        learner = Learner.objects.get(pk=learner_pk)
        notifications_list = list()
        notifications_list.extend(learner.level_up_notifications.order_by('-date')[0:5])
        notifications_list.extend(learner.avatar_evolution_notifications.order_by('-date')[0:5])
        notifications_list.extend(learner.achievement_notifications.order_by('-date')[0:5])
        notifications_list.extend(learner.avatar_achievement_notifications.order_by('date')[0:5])
        notifications_list.extend(learner.level_achievement_notifications.order_by('date')[0:5])
        notifications_list.extend(learner.test_achievement_notifications.order_by('date')[0:5])

        notifications_list.sort(key=lambda x: x.date, reverse=True)
        notifications = list()
        avatar_evolution = list()

        for notification in notifications_list[0:5]:
            if isinstance(notification, AchievementNotification):
                notifications.append({'title': 'Ganaste la versión {} de la insignia {}'.format(notification.version,
                                                                                                notification.badge.name),
                                      'type': notification.type, 'viewed': notification.viewed})
            elif isinstance(notification, AvatarAchievementNotification) \
                    or isinstance(notification, LevelAchievementNotification) \
                    or isinstance(notification, TestAchievementNotification):
                notifications.append({'title': 'Ganaste el logro {}'.format(notification.achievement.name),
                                      'type': notification.type, 'viewed': notification.viewed})
            elif isinstance(notification, LevelUpNotification):
                notifications.append(
                    {'title': 'Subiste al nivel {}'.format(notification.earned_level), 'type': notification.type,
                     'viewed': notification.viewed})
            elif isinstance(notification, AvatarEvolutionNotification):
                notifications.append(
                    {'title': 'Tu avatar llegó a la evolución {}'.format(notification.earned_evolution),
                     'type': notification.type, 'viewed': notification.viewed})
                if not notification.viewed:
                    avatar_evolution.append({'avatar_name': notification.avatar, 'current_evolution': notification.earned_evolution, 'previous_evolution': notification.earned_evolution-1, 'viewed': notification.viewed})
                    notification.viewed = True
                    notification.save()

        return JsonResponse({'notifications': notifications, 'avatar': avatar_evolution})

    def post(self, request):
        learner_pk = request.POST['learner']
        learner = Learner.objects.get(pk=learner_pk)
        notifications_list = list()
        notifications_list.extend(learner.level_up_notifications.filter(viewed=False))
        notifications_list.extend(learner.avatar_evolution_notifications.filter(viewed=False))
        notifications_list.extend(learner.achievement_notifications.filter(viewed=False))
        notifications_list.extend(learner.avatar_achievement_notifications.filter(viewed=False))
        notifications_list.extend(learner.level_achievement_notifications.filter(viewed=False))
        notifications_list.extend(learner.test_achievement_notifications.filter(viewed=False))

        for notification in notifications_list:
            notification.viewed = True
            notification.save()

        return JsonResponse({'ok': 'ok'})


class LearnerExperiencePoints(APIView):
    def get(self, request):
        learner_pk = request.GET['learner']
        learner = Learner.objects.get(pk=learner_pk)
        learner_level = get_learner_level(learner.experience_points)
        next_level = LearnerLevels.objects.get(level=(learner_level.level + 1))
        avatar_points = 0
        avatar = learner.avatar_progresses.get(active=True)
        if avatar.points < 15000:
            avatar_points = avatar.points / 15000
        elif 15000 <= avatar.points < 50000:
            avatar_points = avatar.points / 50000
        elif avatar.points >= 50000:
            avatar_points = 1

        return JsonResponse({'learner_points': (learner.experience_points - learner_level.points),
                             'learner_next_level_points': (next_level.points - learner_level.points),
                             'avatar_points': avatar_points})
