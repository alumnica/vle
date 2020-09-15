from rest_framework import serializers
from alumnica_model.models import ODA, Subject, Reference, Image, MicroODAType, MicroODA, Moment, Content, typeMoment


class EvaluationSerializer(serializers.Serializer):
	question_type = serializers.CharField()
	question_pk = serializers.Field()
	answers = serializers.ListField()

class SubjectSerializer(serializers.ModelSerializer):

	class Meta:
		model = Subject
		fields = [ 'name']		

class ReferenceSerializer(serializers.ModelSerializer):

	class Meta:
		model = Reference
		fields = [ 'name']		


class ImageSerializer(serializers.ModelSerializer):

	class Meta:
		model = Image
		fields = [ 'name', 'file']		



class ODASerializer(serializers.ModelSerializer):	
	subject = SubjectSerializer()
	references = ReferenceSerializer(many=True)
	img_portada = ImageSerializer()
	img_oda = ImageSerializer()
	class Meta:
		model = ODA
		fields = ['id', 'name', 'description', 'subject', 'learning_objective', 'img_portada', 'img_oda', 'references']
		

class MicroodaTypeSerializer(serializers.ModelSerializer):

	class Meta:
		model = MicroODAType
		fields = ['name']


class MicroodaSerializer(serializers.ModelSerializer):
	type = MicroodaTypeSerializer()
	class Meta:
		model = MicroODA
		fields = ['id', 'name',  'type', 'description']


class ContentSerializer(serializers.ModelSerializer):	
	class Meta:
		model = Content
		fields = ['id', 'content',  'url_h5p']



class MomentSerializer(serializers.ModelSerializer):	
	content = ContentSerializer()
	type = serializers.SerializerMethodField()

	class Meta:
		model = Moment
		fields = ['id', 'name',  'type', 'content', 'default_position']

	def get_type(self,obj):
		return obj.get_type_display()
	


