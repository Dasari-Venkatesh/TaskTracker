from rest_framework import serializers
from .models import Team,TeamMember,CustomUser,TaskAssignment,Task

class CustomUserSerializer(serializers.Serializer):
    userid=serializers.IntegerField(read_only = True)
    email = serializers.EmailField()
    firstname=serializers.CharField()
    role=serializers.ChoiceField(choices=CustomUser.ROLES)

    def validate(self, data):
        email=data['email']
        if(CustomUser.objects.filter(email==email)):
            raise serializers.ValidationError("Email exists.")
        validated_data=data
        return validated_data
    def create(self, validated_data):
        user = CustomUser.objects.create(userid=validated_data['userid'],email=validated_data['email'],role = validated_data['role'])
        user.set_password(validated_data['password'])
        user.save()
        return user

    
class TeamSerializer(serializers.Serializer):
    pass

class TaskSerializer(serializers.Serializer):
    pass
