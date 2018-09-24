from django.test import TestCase

from webapp.gamification import get_learner_level


class GetLearnerLevelTestCase(TestCase):
    experience_points_1 = [0, 50, 150, 450, 800, 1820, 2840, 3890, 4990, 6140, 7340, 8590, 9890, 11240,
                           12640, 14090, 15590, 17190, 18890, 20690, 22590, 24590, 26690, 28890, 31190,
                           33590, 36090, 38690, 41390, 44190, 47090, 50090, 53240, 56540, 59990, 63590,
                           67340, 71240, 75290, 79490, 83840, 88340, 92990, 97790, 102740, 107840, 113090,
                           118490, 124040, 129740, 135590, 141590, 147590, 154090, 161090, 168590, 176590,
                           185090, 194090]

    levels_1 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26,
                27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50,
                51, 52, 53, 54, 55, 56, 57, 58, 59]

    experience_points_2 = [203590, 213590, 224090, 235090, 246590, 258590, 271090, 284090, 298090, 313090, 329090,
                           346090, 364090, 383090, 403090, 424090, 446090, 470090, 496090, 524090, 554090, 586090,
                           620090, 656090, 694090, 734090, 776090, 820090, 866090, 914090, 964090, 1016590, 1071590,
                           1129090, 1189090, 1254090, 1324090, 1401590, 1486590, 1586590]

    levels_2 = [60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84,
                85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99]

    def test_first_equation_given_points(self):
        position = 0
        position_errors = []
        error = 0
        for point in self.experience_points_1:
            level = round(get_learner_level(point))
            if level != self.levels_1[position]:
                position_errors.append(point)
                error += 1
            position += 1

        print(error)
        print(position_errors)

    def test_second_equation_given_points(self):
        position = 0
        position_errors = []
        error = 0
        for point in self.experience_points_2:
            level = round(get_learner_level(point))
            if level != self.levels_2[position]:
                position_errors.append(point)
                error += 1
            position += 1

        print(error)
        print(position_errors)