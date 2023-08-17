from .models import CustomUser
from .serializers import CustomUserSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
# Create your views here.

class user_list(APIView):
    
    # List all users, or create new user
    def get(self,request,format = None):
        users = CustomUser.objects.all()
        serializer=CustomUserSerializer(users,many = True)
        return Response(serializer.data)
    
    def post(self, request,format = None):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
    
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