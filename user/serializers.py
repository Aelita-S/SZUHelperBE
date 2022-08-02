from rest_framework import serializers

from user.models import User


class UserLoginSerializer(serializers.ModelSerializer):
    code = serializers.CharField(max_length=50)

    class Meta:
        model = User
        fields = ('code',)


class UserOptionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('config',)
