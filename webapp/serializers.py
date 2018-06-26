
from rest_framework import serializers
from alumnica_model.models.questions import RelationShipQuestion, MultipleOptionQuestion, MultipleAnswerQuestion, \
    NumericQuestion, PullDownListQuestion


class RelationShipQuestionModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = RelationShipQuestion
        fields = '__all__'


class RelationShip(object):
    def __init__(self, relationship, shuffle_answers):
        self.relationship = relationship
        self.shuffle_answers = shuffle_answers


class RelationShipSerializer(serializers.Serializer):
    relationship = RelationShipQuestionModelSerializer()
    shuffle_answers = serializers.ListField()


class MultipleOptionQuestionModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = MultipleOptionQuestion
        fields = '__all__'


class MultipleOption(object):
    def __init__(self, multiple_option, shuffle_answers):
        self.multiple_option = multiple_option
        self.shuffle_answers = shuffle_answers


class MultipleOptionSerializer(serializers.Serializer):
    multiple_option = MultipleOptionQuestionModelSerializer()
    shuffle_answers = serializers.ListField()


class MultipleAnswerQuestionModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = MultipleAnswerQuestion
        fields = '__all__'


class MultipleAnswer(object):
    def __init__(self, multiple_answer, shuffle_answers):
        self.multiple_answer = multiple_answer
        self.shuffle_answers = shuffle_answers


class MultipleAnswerSerializer(serializers.Serializer):
    multiple_answer = MultipleAnswerQuestionModelSerializer()
    shuffle_answers = serializers.ListField()


class NumericQuestionModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = NumericQuestion
        fields = '__all__'


class NumericAnswer(object):
    def __init__(self, pk, shuffle_answers):
        self.numeric = NumericQuestion.objects.get(pk=pk)
        self.shuffle_answers = shuffle_answers


class NumericAnswerSerializer(serializers.Serializer):
    numeric = NumericQuestionModelSerializer(source='*')
    shuffle_answers = serializers.ListField()


class PullDownListQuestionModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = PullDownListQuestion
        fields = '__all__'


class PullDownList(object):
    def __init__(self, pulldown_list, shuffle_answers):
        self.pulldown_list = pulldown_list
        self.shuffle_answers = shuffle_answers


class PullDownListSerializer(serializers.Serializer):
    pulldown_list = PullDownListQuestionModelSerializer()
    shuffle_answers = serializers.ListField()


class EvaluationSerializer(serializers.Serializer):
    relationship = RelationShipSerializer(many=True)
    multiple_option = MultipleOptionSerializer(many=True)
    multiple_answer = MultipleAnswerSerializer(many=True)
    numeric = NumericAnswerSerializer(many=True)
    pulldown_list = PullDownListSerializer(many=True)