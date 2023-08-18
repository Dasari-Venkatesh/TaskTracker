from rest_framework import serializers
from django.shortcuts import get_object_or_404
from .models import Team,TeamMember,CustomUser,TaskAssignment,Task

class CustomUserSerializer(serializers.Serializer):
    userid=serializers.IntegerField(read_only = True)
    email = serializers.EmailField()
    firstname=serializers.CharField()
    role=serializers.ChoiceField(choices=CustomUser.ROLES)
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})

    
    def validate(self, data):
        email=data['email']
        if CustomUser.objects.filter(email__iexact=email).exists():
            raise serializers.ValidationError("Email exists.")
        return data
    
    def create(self, validated_data):
        user = CustomUser.objects.create(email=validated_data['email'],
                                         role = validated_data['role'],
                                         firstname=validated_data.get('firstname',''))
        user.set_password(validated_data['password'])
        user.save()
        return validated_data

    
class TeamSerializer(serializers.ModelSerializer):

    team_members=serializers.SerializerMethodField(read_only = True)
    team_leader=CustomUserSerializer(read_only=True)

    class Meta:
        model = Team
        fields = ['teamid','name','team_leader','team_members']

    def get_team_members(self,object):

        team_members=TeamMember.objects.filter(team=object.teamid)
        lst =[]
        for member in team_members:
            lst.append(CustomUserSerializer(member.user).data)
        return lst
    
    # def to_representation(self, instance):
    #     self.fields['team_leader'] =  CustomUserSerializer(read_only=True)
    #     # self.fields['team_members'] =  CustomUserSerializer(read_only=True)
    #     return super(TeamSerializer, self).to_representation(instance)
    def validate_leader_id(self,value):
        leader = None
        try:
            leader = CustomUser.objects.get(firstname=value)
        except:
            raise serializers.ValidationError("User doesn't exist")
        
        if leader.role != 'teamLead':
            raise serializers.ValidationError("User is not a Team leader")
        
        return leader
    
class TeamMemberSerializer(serializers.ModelSerializer):
    pass

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['taskid','name','team','status']

