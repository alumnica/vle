from alumnica_model.models.progress import LearnerLevels

BASE_UODA_XP = 50
BASE_EVALUATION_XP = 100
DAILY_BONUS_INCREMENT = 0.2
MAX_DAILY_LOGIN = 6
COMPLETED_UODA_INCREMENT = 0.5
REPETITION_PENALTY = [1, 0.5, 0.2, 0]


# first_levels_points = [0, 50, 150, 450, 800, 1820, 2840, 3890, 4990, 6140, 7340]

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


def evaluation_completed_xp(learner):
    pass


def uoda_completed_xp(learner):
    pass
