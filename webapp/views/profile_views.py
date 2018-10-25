from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import redirect, render
from django.utils.datastructures import OrderedSet
from django.views.generic import FormView, UpdateView
from sweetify import sweetify
from django.utils import timezone
from alumnica_model.mixins import OnlyLearnerMixin, LoginCounterMixin
from alumnica_model.models import Badge, MicroODA, LearnerBadgeAchievement, AvatarAchievement, LevelAchievement, \
    TestAchievement, LearnerTestAchievement, ODA, Subject, Ambit
from alumnica_model.models.achievements import TYPE_BADGE_ACHIEVEMENT
from alumnica_model.models.notifications import TestAchievementNotification
from webapp.forms.profile_forms import *
from webapp.gamification import EXPERIENCE_POINTS_CONSTANTS, get_learner_level
from webapp.statement_builders import register_statement, access_statement


class FirstLoginInfoView(LoginRequiredMixin, OnlyLearnerMixin, LoginCounterMixin, FormView):
    """
    Personal information quiz view
    """
    login_url = 'login_view'
    template_name = 'webapp/pages/first-login-info.html'
    form_class = FirstLoginInfoForm

    def form_valid(self, form):
        user = AuthUser.objects.get(email=self.request.user.email)
        form.save_form(user)
        timestamp = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc).isoformat()
        register_statement(request=self.request, timestamp=timestamp, user=user)
        if self.request.user.profile.learning_style is None:
            return redirect(to='first-login-p1_view')
        return redirect(to='dashboard_view')


class FirstLoginP1View(LoginRequiredMixin, OnlyLearnerMixin, LoginCounterMixin, FormView):
    """
    Short Learning style quiz view
    """
    login_url = 'login_view'
    template_name = 'webapp/pages/first-login-p1.html'
    form_class = FirstLoginP1
    first_selection = '0'
    second_selection = '0'

    def form_valid(self, form):
        self.first_selection = self.request.POST.get('pregunta-2set')
        self.second_selection = self.request.POST.get('pregunta-3set')
        form.save_form(self.request.user, self.first_selection, self.second_selection)
        return redirect(to='dashboard_view')


class LargeLearningStyleQuizView(LoginRequiredMixin, OnlyLearnerMixin, LoginCounterMixin, FormView):
    """
    Large Learning style quiz view
    """
    login_url = 'login_view'
    form_class = LargeLearningStyleQuizForm
    template_name = 'webapp/pages/user-test.html'

    def dispatch(self, request, *args, **kwargs):
        response = super(LargeLearningStyleQuizView, self).dispatch(request, *args, **kwargs)
        if response.status_code == 200 and request.method == 'GET':
            timestamp = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc).isoformat()
            access_statement(request, 'Large Learning Style Quiz', timestamp)
        return response

    def form_valid(self, form):
        answers = self.request.POST['test-answers'].split(',')
        letters = {'a': 0, 'b': 1, 'c': 2, 'd': 3}
        answers_numbers = [0, 0, 0, 0]
        for answer in answers:
            answers_numbers[letters[answer]] += 1

        if answers_numbers[0] > answers_numbers[1] and answers_numbers[3] > answers_numbers[2]:
            self.request.user.profile.learning_style = LearningStyle.objects.get(name='Acomodador')
        elif answers_numbers[1] > answers_numbers[0] and answers_numbers[2] > answers_numbers[3]:
            self.request.user.profile.learning_style = LearningStyle.objects.get(name='Asimilador')
        elif answers_numbers[0] > answers_numbers[1] and answers_numbers[2] > answers_numbers[3]:
            self.request.user.profile.learning_style = LearningStyle.objects.get(name='Divergente')
        elif answers_numbers[1] > answers_numbers[2] and answers_numbers[3] > answers_numbers[2]:
            self.request.user.profile.learning_style = LearningStyle.objects.get(name='Convergente')

        if not self.request.user.profile.large_quiz_completed:
            test_achievement = TestAchievement.objects.get(name='Completa el Test de aprendizaje')
            LearnerTestAchievement.objects.create(learner=self.request.user.profile, achievement=test_achievement)
            TestAchievementNotification.objects.create(learner=self.request.user.profile, achievement=test_achievement)
            self.request.user.profile.assign_xp(test_achievement.xp)
            self.request.user.profile.large_quiz_completed = True
            self.request.user.profile.assign_xp(EXPERIENCE_POINTS_CONSTANTS['learning_large_quiz'])
            timestamp = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc).isoformat()
            learning_experience_received(user=self.request.user,
                                         object_type='Learning Style Quiz',
                                         object_name=self.request.user.profile.learning_style.name,
                                         timestamp=timestamp,
                                         gained_xp=EXPERIENCE_POINTS_CONSTANTS['learning_large_quiz'])

        self.request.user.profile.save()

        return redirect(to='dashboard_view')


class ProfileSettingsView(LoginRequiredMixin, OnlyLearnerMixin, LoginCounterMixin, UpdateView):
    """
    Edit personal information view
    """
    login_url = 'login_view'
    template_name = 'webapp/pages/user-profile.html'
    form_class = ProfileSettingsForm

    def dispatch(self, request, *args, **kwargs):
        response = super(ProfileSettingsView, self).dispatch(request, *args, **kwargs)
        if response.status_code == 200 and request.method == 'GET':
            timestamp = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc).isoformat()
            access_statement(request, 'Profile', timestamp)
        return response

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super(ProfileSettingsView, self).get_context_data(**kwargs)
        learner = self.object.profile
        learner_name = '{} {}'.format(self.object.first_name, self.object.profile.last_name)
        level = get_learner_level(learner.experience_points)
        badges = self.get_badges()
        achievements = self.get_achievements()
        notifications = self.get_notifications()

        avatares = list()
        avatar_active = None

        for avatar in learner.avatar_progresses.all():
            avatar_level = 3
            if avatar.points <= 50000:
                if avatar.points <= 15000:
                    avatar_level = 1
                elif 15000 < avatar.points <= 50000:
                    avatar_level = 2

            if not avatar.active:
                avatares.append({'name': avatar.avatar_name, 'level': avatar_level})
            else:
                avatar_active = {'name': avatar.avatar_name, 'level': avatar_level}

        context.update({'level': level, 'learner_name': learner_name, 'badges': badges, 'achievements': achievements,
                        'notifications': notifications, 'avatares': avatares, 'avatar_active': avatar_active})
        return context

    def form_invalid(self, form):
        if form['new_password'].errors:
            sweetify.error(self.request, form.errors['new_password'][0], persistent='Ok')
        elif form['new_password_confirmation'].errors:
            sweetify.error(self.request, form.errors['new_password_confirmation'][0], persistent='Ok')
        elif form['previous_password'].errors:
            sweetify.error(self.request, form.errors['previous_password'][0], persistent='Ok')

        context = self.get_context_data()
        return render(self.request, self.template_name, context=context)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')
        return redirect('profile_view')

    def get_badges(self):
        badges = []
        learner = self.object.profile
        for badge_achievement in learner.badge_achievements.exclude(version=0):
            version = badge_achievement.version
            badge = badge_achievement.badge
            ambit = badge.ambit.first()
            image = badge.first_version
            if version == 2:
                image = badge.second_version
            elif version == 3:
                image = badge.third_version

            badges.append({'name': badge.name, 'version': version, 'image': image, 'pk': badge.pk})

        return badges

    def get_achievements(self):
        achievements = []
        learner = self.object.profile

        for achievement in AvatarAchievement.objects.all():
            earned = 0
            if learner.avatar_achievements.filter(achievement=achievement).exists():
                earned = 1
            achievements.append(
                {'name': achievement.name, 'type': achievement.type, 'pk': achievement.pk, 'earned': earned,
                 'description': '+ {} xp'.format(achievement.xp)})

        for achievement in LevelAchievement.objects.all():
            earned = 0
            if learner.level_achievements.filter(achievement=achievement).exists():
                earned = 1
            achievements.append(
                {'name': achievement.name, 'type': achievement.type, 'pk': achievement.pk, 'earned': earned,
                 'description': '+ {} xp'.format(achievement.xp)})

        for achievement in TestAchievement.objects.all():
            earned = 0
            if learner.test_achievements.filter(achievement=achievement).exists():
                earned = 1
            achievements.append(
                {'name': achievement.name, 'type': achievement.type, 'pk': achievement.pk, 'earned': earned,
                 'description': '+ {} xp'.format(achievement.xp)})

        microodas = OrderedSet(MicroODA.objects.filter(
            activities__in=[progress.activity for progress in
                            learner.activities_progresses.filter(is_complete=True)]))
        odas_with_evaluation = learner.get_completed_odas(microodas=microodas)
        subjects_completed = learner.get_completed_subjects(odas_with_evaluation)
        ambits_completed = learner.get_completed_ambits(subjects_completed)

        for badge in Badge.objects.all():
            ambit = badge.ambit.first()
            if ambit is not None and ambit.is_published:
                microoda_total_counter = MicroODA.objects.exclude(
                    oda__zone=0).filter(oda__subject__ambit__pk=ambit.pk).count()
                microoda_learner_counter = len(OrderedSet(MicroODA.objects.filter(
                    activities__in=[progress.activity for progress in
                                    learner.activities_progresses.filter(
                                        Q(is_complete=True) & Q(activity__microoda__oda__subject__ambit=ambit))])))

                learner_achievement, created = LearnerBadgeAchievement.objects.get_or_create(learner=learner,
                                                                                             badge=badge)

                # For first version
                total_version_counter = round(microoda_total_counter * 0.2)
                learner_version_counter = microoda_learner_counter
                earned = 0
                image = badge.first_version

                if learner_achievement.version > 0:
                    earned = 1
                if total_version_counter < learner_version_counter:
                    learner_counter = total_version_counter
                else:
                    learner_counter = learner_version_counter
                achievements.append(
                    {'name': badge.name, 'image': image, 'type': TYPE_BADGE_ACHIEVEMENT, 'pk': badge.pk,
                     'version': learner_achievement.version,
                     'description': 'Completa {} µODAS del {}'.format(total_version_counter, badge.name),
                     'uodas': '{}|{}'.format(learner_counter, total_version_counter), 'earned': earned})

                # Second version
                image = learner_achievement.badge.second_version
                total_version_counter = round(microoda_total_counter * 0.5)
                earned = 0
                if learner_achievement.version > 1:
                    earned = 1
                if total_version_counter < learner_version_counter:
                    learner_counter = total_version_counter
                else:
                    learner_counter = learner_version_counter
                achievements.append(
                    {'name': badge.name, 'image': image, 'type': TYPE_BADGE_ACHIEVEMENT, 'pk': badge.pk,
                     'version': learner_achievement.version,
                     'description': 'Completa {} µODAS del {}'.format(total_version_counter, badge.name),
                     'uodas': '{}|{}'.format(learner_counter, total_version_counter), 'earned': earned})

                # Third version
                image = learner_achievement.badge.third_version
                total_version_counter = microoda_total_counter
                earned = 0
                if learner_achievement.version > 2:
                    earned = 1

                achievements.append(
                    {'name': badge.name, 'image': image, 'type': TYPE_BADGE_ACHIEVEMENT, 'pk': badge.pk,
                     'version': learner_achievement.version,
                     'description': 'Completa {} µODAS del {}'.format(total_version_counter, badge.name),
                     'uodas': '{}|{}'.format(learner_version_counter, total_version_counter), 'earned': earned})

            else:
                learner_achievement, created = LearnerBadgeAchievement.objects.get_or_create(learner=learner,
                                                                                             badge=badge)

                if badge.name == 'ODAs 100%':
                    description = 'Completa {} odas'
                    learner_total_counter = len(learner.get_completed_odas(microodas=microodas, with_evaluation=False))
                    badge_total_counter = ODA.objects.exclude(Q(zone=0) | Q(subject__ambit__is_published=False)).count()
                    achievements.extend(
                        self.get_achievement_to_add(badge_total_counter, learner_achievement, badge, description,
                                                    learner_total_counter))

                elif badge.name == 'ODAs completadas':
                    badge_total_counter = ODA.objects.exclude(Q(zone=0) | Q(subject__ambit__is_published=False)).count()
                    learner_total_counter = len(odas_with_evaluation)
                    description = 'Completa {} odas y sus evaluaciones'

                    achievements.extend(
                        self.get_achievement_to_add(badge_total_counter, learner_achievement, badge, description,
                                                    learner_total_counter))

                elif badge.name == 'Días consecutivos iniciando sesión':
                    badge_total_counter = 30
                    learner_total_counter = learner.login_progress.login_counter
                    description = 'Inicia sesión {} días seguidos'

                    achievements.extend(
                        self.get_achievement_to_add(badge_total_counter, learner_achievement, badge, description,
                                                    learner_total_counter))

                elif badge.name == 'Materias 100%':
                    badge_total_counter = Subject.objects.exclude(ambit__is_published=False).count()
                    learner_total_counter = len(subjects_completed)
                    description = 'Completa {} materias'

                    achievements.extend(
                        self.get_achievement_to_add(badge_total_counter, learner_achievement, badge, description,
                                                    learner_total_counter))

                elif badge.name == 'Ambitos 100%':
                    badge_total_counter = Ambit.objects.exclude(is_published=False).count()
                    learner_total_counter = len(ambits_completed)
                    description = 'Completa {} ámbitos'

                    achievements.extend(
                        self.get_achievement_to_add(badge_total_counter, learner_achievement, badge, description,
                                                    learner_total_counter))

        return achievements

    def get_achievement_to_add(self, badge_total_counter, learner_achievement, badge, description,
                               learner_version_counter):

        achievements = list()
        # First version
        image = badge.first_version
        total_version_counter = round(badge_total_counter * 0.2)
        earned = 0

        if learner_achievement.version > 0:
            earned = 1
        if total_version_counter < learner_version_counter:
            learner_counter = total_version_counter
        else:
            learner_counter = learner_version_counter
        achievements.append(
            {'name': badge.name, 'image': image, 'type': TYPE_BADGE_ACHIEVEMENT, 'pk': badge.pk,
             'version': learner_achievement.version,
             'description': description.format(total_version_counter),
             'uodas': '{}|{}'.format(learner_counter, total_version_counter), 'earned': earned})

        # Second version
        earned = 0
        image = learner_achievement.badge.second_version
        total_version_counter = round(badge_total_counter * 0.5)

        if learner_achievement.version > 1:
            earned = 1
        if total_version_counter < learner_version_counter:
            learner_counter = total_version_counter
        else:
            learner_counter = learner_version_counter
        achievements.append(
            {'name': badge.name, 'image': image, 'type': TYPE_BADGE_ACHIEVEMENT, 'pk': badge.pk,
             'version': learner_achievement.version,
             'description': description.format(total_version_counter),
             'uodas': '{}|{}'.format(learner_counter, total_version_counter), 'earned': earned})

        # Third version
        earned = 0
        image = learner_achievement.badge.third_version
        total_version_counter = badge_total_counter

        if learner_achievement.version > 2:
            earned = 1
        achievements.append(
            {'name': badge.name, 'image': image, 'type': TYPE_BADGE_ACHIEVEMENT, 'pk': badge.pk,
             'version': learner_achievement.version,
             'description': description.format(total_version_counter),
             'uodas': '{}|{}'.format(learner_version_counter, total_version_counter), 'earned': earned})

        return achievements

    def get_notifications(self):
        learner = self.object.profile
        notifications = []
        current_datetime = timezone.now()
        for notification in learner.achievement_notifications.all():
            time_diff = current_datetime - notification.date
            notifications.append({'object': 'Versión {}'.format(notification.version),
                                  'description': 'Obtuviste nueva version de la insignia {}'.format(
                                      notification.badge.name), 'days': time_diff.days, 'viewed': notification.viewed,
                                  'type': notification.type, 'date': notification.date})
        for notification in learner.avatar_evolution_notifications.all():
            time_diff = current_datetime - notification.date
            notifications.append(
                {'object': notification.earned_evolution, 'description': 'Tu avatar evolucionó de nivel',
                 'days': time_diff.days, 'viewed': notification.viewed, 'type': notification.type,
                 'date': notification.date})
        for notification in learner.uoda_completed_notifications.all():
            time_diff = current_datetime - notification.date
            notifications.append({'object': '{} XP'.format(notification.xp),
                                  'description': 'Completaste una MicroODA de la ODA {}'.format(
                                      notification.microoda.oda.name), 'days': time_diff.days,
                                  'viewed': notification.viewed, 'type': notification.type, 'date': notification.date})
        for notification in learner.evaluation_completed_notifications.all():
            time_diff = current_datetime - notification.date
            notifications.append({'object': '{} de score'.format(notification.score),
                                  'description': 'Completaste la evaluación de la ODA {}'.format(
                                      notification.evaluation.oda.first().name), 'days': time_diff.days,
                                  'viewed': notification.viewed, 'type': notification.type, 'date': notification.date})
        for notification in learner.level_up_notifications.all():
            time_diff = current_datetime - notification.date
            notifications.append(
                {'object': 'Nivel {}'.format(notification.earned_level), 'description': 'Subiste de nivel!',
                 'days': time_diff.days, 'viewed': notification.viewed, 'type': notification.type,
                 'date': notification.date})
        for notification in learner.test_achievement_notifications.all():
            time_diff = current_datetime - notification.date
            notifications.append(
                {'object': 'Logro ganado!', 'description': notification.achievement.name,
                 'days': time_diff.days, 'viewed': notification.viewed, 'type': notification.type,
                 'date': notification.date})
        for notification in learner.level_achievement_notifications.all():
            time_diff = current_datetime - notification.date
            notifications.append(
                {'object': 'Logro ganado!', 'description': notification.achievement.name,
                 'days': time_diff.days, 'viewed': notification.viewed, 'type': notification.type,
                 'date': notification.date})
        for notification in learner.avatar_achievement_notifications.all():
            time_diff = current_datetime - notification.date
            notifications.append(
                {'object': 'Logro ganado!', 'description': notification.achievement.name,
                 'days': time_diff.days, 'viewed': notification.viewed, 'type': notification.type,
                 'date': notification.date})
        notifications.sort(key=lambda x: x['date'], reverse=False)
        return notifications
