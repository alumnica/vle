first_levels_points = [0, 50, 150, 450, 800, 1820, 2840, 3890, 4990, 6140, 7340]


def get_learner_level(experience_points):
    level = 100
    x = experience_points
    if x <= 7340:
        for points in first_levels_points:
            if points >= x:
                if points == x:
                    return first_levels_points.index(points) + 1
                else:
                    return first_levels_points.index(points)

    elif 7340 < x <= 194090:
        level = (1.224e-24 * (x ** 5)) - (6.924e-19 * (x ** 4)) + (1.491e-13 * (x ** 3)) - (1.584e-8 * (x ** 2)) + (
                    1.072e-3 * x) + 3.421
    elif 194090 < x <= 1586590:
        level = (-2.751e-23 * (x ** 4)) + (1.16e-16 * (x ** 3)) - (1.848e-10 * (x ** 2)) + (1.502e-4 * x) + 36.55

    return level
