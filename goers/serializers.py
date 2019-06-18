from django.contrib.auth.models import User, Group
from rest_framework import serializers
from goers.models import Recommendation, Training

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')

class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')

class TrainingSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Training
        fields = ('algorithm', 'test_size', 'train_accuracy', 'test_accuracy')

class RecommendationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Recommendation
        fields = ('prediction', 'description')