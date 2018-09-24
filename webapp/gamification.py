from alumnica_model.models.content import MicroODAByLearningStyle
from alumnica_model.models.progress import LearnerLevels

BASE_UODA_XP = 50
BASE_EVALUATION_XP = 100
DAILY_BONUS_INCREMENT = 0.2
MAX_DAILY_LOGIN = 6
COMPLETED_UODA_INCREMENT = 0.5
REPETITION_PENALTY = [1, 0.5, 0.2, 0]


# first_levels_points = [0, 50, 150, 450, 800, 1820, 2840, 3890, 4990, 6140, 7340]

def get_daily_bonus(login_counter):
    if login_counter < MAX_DAILY_LOGIN:
        return DAILY_BONUS_INCREMENT * login_counter + (1 - DAILY_BONUS_INCREMENT)
    else:
        return DAILY_BONUS_INCREMENT * MAX_DAILY_LOGIN + (1 - DAILY_BONUS_INCREMENT)


def get_learner_level(experience_points):
    level = LearnerLevels.objects.last()
    # x = experience_points

    learner_levels = LearnerLevels.objects.all()

    for level_object in learner_levels:
        if level_object.points >= experience_points:
            if level_object.points == experience_points:
                level = level_object
            else:
                level = learner_levels.get(level=(level.level - 1))

    # if x <= 7340:
    #     for points in first_levels_points:
    #         if points >= x:
    #             if points == x:
    #                 return first_levels_points.index(points) + 1
    #             else:
    #                 return first_levels_points.index(points)
    #
    # elif 7340 < x <= 194090:
    #     level = (1.224e-24 * (x ** 5)) - (6.924e-19 * (x ** 4)) + (1.491e-13 * (x ** 3)) - (1.584e-8 * (x ** 2))
    # + (1.072e-3 * x) + 3.421
    # elif 194090 < x <= 1586590:
    #     level = (-2.751e-23 * (x ** 4)) + (1.16e-16 * (x ** 3)) - (1.848e-10 * (x ** 2)) + (1.502e-4 * x) + 36.55

    return level


def evaluation_completed_xp(learner, oda):
    pen_rep = 0
    completed_uodas = 0
    daily_bonus = get_daily_bonus(learner.login_progress.login_counter)
    for uoda in oda.microodas.all():
        if learner.activities_progresses.get(activity=uoda.activities.first()).is_complete:
            completed_uodas += 1

    learner_completed_counter = learner.evaluations_progresses.get(
        evaluation=oda.evaluation).evaluation_completed_counter
    if learner_completed_counter < 4:
        pen_rep = REPETITION_PENALTY[learner_completed_counter]

    bonus_eval = (COMPLETED_UODA_INCREMENT * completed_uodas) + 1

    return BASE_EVALUATION_XP * daily_bonus * bonus_eval * pen_rep


def uoda_completed_xp(learner, oda):
    # BASE_UODA_XP * daily_bonus * BonusEA * PenRep
    pen_rep = 0
    daily_bonus = get_daily_bonus(learner.login_progress.login_counter)

    oda_sequencing = learner.odas_sequence_progresses.get(oda=oda)

    position = 0
    sequencing = MicroODAByLearningStyle[learner.learning_style.name]

    bonus_ea = 2

    for uoda in oda_sequencing.uoda_progress_order.split('|'):
        if sequencing[position] != uoda:
            bonus_ea = 1
            break
        position += 1

    learner_completed_counter = learner.activities_progresses.get(
        activity=oda.microodas.first().activities.first()).activity_completed_counter
    if learner_completed_counter < 4:
        pen_rep = REPETITION_PENALTY[learner_completed_counter]

    return BASE_UODA_XP * daily_bonus * bonus_ea * pen_rep
