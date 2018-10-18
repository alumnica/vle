from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import redirect, render
from django.utils.datastructures import OrderedSet
from django.views.generic import FormView, UpdateView
from sweetify import sweetify

from alumnica_model.mixins import OnlyLearnerMixin, LoginCounterMixin
from alumnica_model.models import Badge, MicroODA, LearnerBadgeAchievement, AvatarAchievement, LevelAchievement, \
    TestAchievement
from alumnica_model.models.achievements import TYPE_BADGE_ACHIEVEMENT
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
        return redirect(to='first-login-p1_view')


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

        experience_pts = self.object.profile.experience_points

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
            if learner.avatar_achievements.filter(pk=achievement.pk).exists():
                earned = 1
            achievements.append(
                {'name': achievement.name, 'type': achievement.type, 'pk': achievement.pk, 'earned': earned,
                 'description': '+ {} xp'.format(achievement.xp)})

        for achievement in LevelAchievement.objects.all():
            earned = 0
            if learner.level_achievements.filter(pk=achievement.pk).exists():
                earned = 1
            achievements.append(
                {'name': achievement.name, 'type': achievement.type, 'pk': achievement.pk, 'earned': earned,
                 'description': '+ {} xp'.format(achievement.xp)})

        for achievement in TestAchievement.objects.all():
            earned = 0
            if learner.test_achievements.filter(pk=achievement.pk).exists():
                earned = 1
            achievements.append(
                {'name': achievement.name, 'type': achievement.type, 'pk': achievement.pk, 'earned': earned,
                 'description': '+ {} xp'.format(achievement.xp)})

        for badge in Badge.objects.all():
            ambit = badge.ambit.first()
            if ambit is not None and ambit.is_published:
                microoda_total_counter = MicroODA.objects.exclude(
                    oda__zone=0).filter(oda__subject__ambit__pk=ambit.pk).count()
                microoda_learner_counter = len(
                    OrderedSet([progress.activity for progress in learner.activities_progresses.filter(
                        Q(is_complete=True) & Q(activity__microoda__oda__subject__ambit=ambit))]))
                image = badge.first_version
                learner_achievement, created = LearnerBadgeAchievement.objects.get_or_create(learner=learner, badge=badge)
                total_version_counter = 0
                learner_version_counter = 0

                if learner_achievement.version == 0:
                    total_version_counter = round(microoda_total_counter * 0.2)
                    learner_version_counter = microoda_learner_counter
                elif learner_achievement.version == 1:
                    image = learner_achievement.badge.second_version
                    total_version_counter = round(microoda_total_counter * 0.5) - round(microoda_total_counter * 0.2)
                    learner_version_counter = round(microoda_learner_counter - (microoda_total_counter * 0.2))
                elif learner_achievement.version == 2:
                    image = learner_achievement.badge.third_version
                    total_version_counter = microoda_total_counter - round(microoda_total_counter * 0.5)
                    learner_version_counter = round(microoda_learner_counter - (microoda_total_counter * 0.5))
                elif learner_achievement.version == 3:
                    total_version_counter = microoda_total_counter
                    learner_version_counter = microoda_learner_counter

                achievements.append(
                    {'name': badge.name, 'image': image, 'type': TYPE_BADGE_ACHIEVEMENT, 'pk': badge.pk,
                     'version': learner_achievement.version,
                     'description': 'Completa {} µODAS del {}'.format(total_version_counter, badge.name),
                     'uodas': '{}|{}'.format(learner_version_counter, total_version_counter)})

            else:
                learner_achievement, created = LearnerBadgeAchievement.objects.get_or_create(learner=learner, badge=badge)
                uoda_total = MicroODA.objects.exclude(Q(oda__zone=0) | Q(oda__subject__ambit__is_published=False))
                learner_total_counter = 0
                badge_total_counter = 0
                description = ''
                image = badge.first_version
                if badge.name == 'ODAs 100%':
                    badge_total_counter = uoda_total.count()
                    learner_total_counter = len(learner.get_completed_odas(with_evaluation=False))
                    description = 'Completa {} odas'

                elif badge.name == 'ODAs completadas':
                    badge_total_counter = len(OrderedSet([microoda.oda for microoda in uoda_total]))
                    learner_total_counter = len(learner.get_completed_odas())
                    description = 'Completa {} odas y sus evaluaciones'

                elif badge.name == 'Días consecutivos iniciando sesión':
                    badge_total_counter = 30
                    learner_total_counter = learner.login_progress.login_counter
                    description = 'Inicia sesión {} días seguidos'

                elif badge.name == 'Materias 100%':
                    badge_total_counter = len(OrderedSet([microoda.oda.subject for microoda in uoda_total]))
                    learner_total_counter = len(learner.get_completed_subjects())
                    description = 'Completa {} materias'

                elif badge.name == 'Ambitos 100%':
                    badge_total_counter = len(OrderedSet([microoda.oda.subject.ambit for microoda in uoda_total]))
                    learner_total_counter = len(learner.get_completed_ambits())
                    description = 'Completa {} ámbitos'

                total_version_counter = 0
                learner_version_counter = 0

                if learner_achievement.version == 0:
                    total_version_counter = round(badge_total_counter * 0.2)
                    learner_version_counter = learner_total_counter
                elif learner_achievement.version == 1:
                    image = learner_achievement.badge.second_version
                    total_version_counter = round(badge_total_counter * 0.5) - round(
                        badge_total_counter * 0.2)
                    learner_version_counter = round(learner_total_counter - (badge_total_counter * 0.2))
                elif learner_achievement.version == 2:
                    image = learner_achievement.badge.third_version
                    total_version_counter = badge_total_counter - round(badge_total_counter * 0.5)
                    learner_version_counter = round(learner_total_counter - (badge_total_counter * 0.5))
                elif learner_achievement.version == 3:
                    image = learner_achievement.badge.third_version
                    total_version_counter = badge_total_counter
                    learner_version_counter = learner_total_counter

                achievements.append(
                    {'name': badge.name, 'image': image, 'type': TYPE_BADGE_ACHIEVEMENT, 'pk': badge.pk,
                     'version': learner_achievement.version,
                     'description': description.format(total_version_counter),
                     'uodas': '{}|{}'.format(learner_version_counter, total_version_counter)})

        return achievements

    def get_notifications(self):
        learner = self.object.profile
        notifications = []

        for notification in learner.achievement_notifications.all():
            notifications.append({'object': 'Versión {}'.format(notification.version), 'description': 'Obtuviste nueva version de la insignia {}'.format(notification.badge.name), 'date': notification.date, 'viewed': notification.viewed, 'type': notification.type})
        for notification in learner.avatar_evolution_notifications.all():
            notifications.append({'object': notification.earned_evolution, 'description': 'Tu avatar evolucionó de nivel', 'date': notification.date, 'viewed': notification.viewed, 'type': notification.type})
        for notification in learner.uoda_completed_notifications.all():
            notifications.append({'object': '{} XP'.format(notification.xp), 'description': 'Completaste una MicroODA de la ODA {}'.format(notification.microoda.oda.name), 'date': notification.date, 'viewed': notification.viewed, 'type': notification.type})
        for notification in learner.evaluation_completed_notifications.all():
            notifications.append({'object': '{} de score'.format(notification.score), 'description': 'Completaste la evaluación de la ODA {}'.format(notification.evaluation.oda.name), 'date': notification.date, 'viewed': notification.viewed, 'type': notification.type})
        for notification in learner.level_up_notifications.all():
            notifications.append({'object': 'Nivel {}'.format(notification.earned_level), 'description': 'Subiste de nivel!', 'date': notification.date, 'viewed': notification.viewed, 'type': notification.type})
        return notifications
