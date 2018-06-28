
from rest_framework import serializers

class EvaluationSerializer(serializers.Serializer):
    question_type = serializers.CharField()
    question_pk = serializers.Field()
    answers = serializers.ListField()