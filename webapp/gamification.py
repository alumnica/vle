from alumnica_model.models.content import MicroODAByLearningStyle
from alumnica_model.models.users import LearnerLevels

EXPERIENCE_POINTS_CONSTANTS = {
    'learning_large_quiz': 2000,
    'profile_updated': 100,

}

BASE_UODA_XP = 50
BASE_EVALUATION_XP = 100
DAILY_BONUS_INCREMENT = 0.2
MAX_DAILY_LOGIN = 6
COMPLETED_UODA_INCREMENT = 0.5
REPETITION_PENALTY = [1, 0.5, 0.2, 0]


# first_levels_points = [0, 50, 150, 450, 800, 1820, 2840, 3890, 4990, 6140, 7340]

def get_daily_bonus(login_counter):
    """
    Gets daily bonus points
    :param login_counter: Login counter
    """
    if login_counter < MAX_DAILY_LOGIN:
        return DAILY_BONUS_INCREMENT * login_counter + (1 - DAILY_BONUS_INCREMENT)
    else:
        return DAILY_BONUS_INCREMENT * MAX_DAILY_LOGIN + (1 - DAILY_BONUS_INCREMENT)


def get_learner_level(experience_points):
    """
    Gets current learner level
    :param experience_points: learner experience points
    """
    level = LearnerLevels.objects.first()
    learner_levels = LearnerLevels.objects.all()

    for level_object in learner_levels:
        if level_object.points >= experience_points:
            if level_object.points == experience_points:
                level = level_object
                break
            else:
                level = learner_levels.get(level=(level_object.level - 1))
                break
    return level


def evaluation_completed_xp(login_counter, completed_uodas, completed_counter):
    """
    Gets experience points to add after completing evaluation
    :param login_counter: learner login counter
    :param completed_uodas: completed MicroODAs learner learner
    :param completed_counter: completed MicroODAs learner evaluation counter
    :return: xp, multipliers equation
    """
    pen_rep = 0
    daily_bonus = get_daily_bonus(login_counter)

    if completed_counter < 4:
        pen_rep = REPETITION_PENALTY[completed_counter - 1]

    bonus_eval = (COMPLETED_UODA_INCREMENT * completed_uodas) + 1

    equation = {'base_xp': BASE_EVALUATION_XP,
                'daily_bonus': round(daily_bonus, 2),
                'bonus_eval': round(bonus_eval, 2),
                'pen_rep': pen_rep}

    return round(BASE_EVALUATION_XP * daily_bonus * bonus_eval * pen_rep), equation


def uoda_completed_xp(login_counter, oda_sequencing, learning_style, completed_counter):
    """
    Gets experience points to add after completing MicroODA
    :param login_counter: learner login counter
    :param oda_sequencing: learner microoda completed sequence
    :param learning_style: learner learnign style
    :param completed_counter: completed MicroODa learner counter
    :return: xp, multipliers equation
    """
    # BASE_UODA_XP * daily_bonus * BonusEA * PenRep
    pen_rep = 0
    daily_bonus = get_daily_bonus(login_counter)

    position = 0
    sequencing = MicroODAByLearningStyle[learning_style]

    bonus_ea = 2

    for uoda in oda_sequencing.strip().split(' '):
        if sequencing[position] != uoda:
            bonus_ea = 1
            break
        position += 1

    if completed_counter <= 4:
        pen_rep = REPETITION_PENALTY[completed_counter - 1]

    equation = {'base_xp': BASE_UODA_XP,
                'daily_bonus': round(daily_bonus, 2),
                'bonus_ea': round(bonus_ea, 2),
                'pen_rep': pen_rep}

    return round(BASE_UODA_XP * daily_bonus * bonus_ea * pen_rep), equation
