from .models import (CustomUser,
                     Task,
                     Team,
    )
from .serializers import (CustomUserSerializer,
                          TaskSerializer,
                          TeamSerializer
    )
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
# Create your views here.


class user_list(APIView):
    
    # List all users, or create new user
    def get(self,request,format = None):
        users = CustomUser.objects.all()
        serializer=CustomUserSerializer(users,many = True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            # print(request.data)
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors)
    
class user_view(APIView):
    def get_object(self,pk):
        try:
            return CustomUser.objects.get(pk=pk)
        except CustomUser.DoesNotExist:
            raise Http404
    def get(self,request,pk,format=None):
        user=self.get_object(pk)
        serializer=CustomUserSerializer(user)
        return Response(serializer.data)
    
    # Handle user update (HTTP PUT request)
    def put(self, request, pk, format=None):
        user = self.get_object(pk)
        serializer = CustomUserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Handle user deletion (HTTP DELETE request)
    def delete(self, request, pk, format=None):
        user = self.get_object(pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def patch(self, request, pk, format=None):
        user = self.get_object(pk)
        serializer = CustomUserSerializer(user, data=request.data, partial=True)  # Note the `partial=True` here
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class task_list(APIView):
    def get(self,request,format = None):
        tasks = Task.objects.all()
        serializer=TaskSerializer(tasks,many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            # print(request.data)
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors)

class task_view(APIView):
    def get_object(self,pk):
        try:
            return Task.objects.get(pk=pk)
        except Task.DoesNotExist:
            raise Http404
    def get(self,request,pk):
        task=self.get_object(pk)
        serializer=TaskSerializer(task)
        return Response(serializer.data)
    
class team_list(APIView):
    def get(self,request):
        teams = Team.objects.all()
        serializer=TeamSerializer(teams,many=True)
        return Response(serializer.data)
    
    
    # {   "name":"Scripting",
    #       "team_leader":"das"
    # }
    def post(self, request):
        data=request.data
        # print(data)
        team_lead_name=data['team_leader']
        # print(team_lead_name)
        team_leader=get_object_or_404(CustomUser,firstname=team_lead_name,role='team leader')
        print("note here:",team_leader)
        serializer = TeamSerializer(data=data)
        # print(request.data)
        if serializer.is_valid():
            serializer.save(team_leader=team_leader)
            # print(request.data)
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors)

class team_view(APIView):
    def get_object(self,pk):
        try:
            return Team.objects.get(pk=pk)
        except Team.DoesNotExist:
            raise Http404
    def get(self,request,pk):
        team=self.get_object(pk)
        serializer=TeamSerializer(team)
        return Response(serializer.data)

"""
def users_list(request):
    
    # List all users, or create a new users.
    
    if request.method == 'GET':
        employees = CustomUser.objects.all()
        serializer = CustomUserSerializer(employees, many=True)
        return JsonResponse(serializer.data, safe=False)
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = CustomUserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)
    
"""