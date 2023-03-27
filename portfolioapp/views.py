from django.shortcuts import render
from rest_framework.response import Response
from django.http import HttpResponseRedirect
from rest_framework import generics
from django.contrib.auth import authenticate, login, logout
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .serializer import UserDataSerializer, EmploymentSerializer, HobbySerializer
from .models import UserData, Employment, Hobby

def login_view(request):
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
    
    return render(request, 'registration/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')

def signup(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/')
  
    form = UserCreationForm()
    
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return HttpResponseRedirect('/')
        
    return render(request, 'registration/signup.html', {'form': form} )

class UserDataList(APIView,IsAuthenticated):
    
    serilizer_class = UserDataSerializer
    
    def get(self, request):
        all_users = UserData.objects.all()
        serializer = UserDataSerializer(all_users, many=True)
        return Response(serializer.data,200)
    
    def post(self, request):
        serializer = UserDataSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data,200)
    
class SingleUserDataList(generics.RetrieveUpdateDestroyAPIView, IsAuthenticated):
    queryset = UserData.objects.all()
    serializer_class = UserDataSerializer 
     
    
class Employments(APIView,IsAuthenticated):
    serilizer_class = EmploymentSerializer
    
    def get(self, request):
        all_users = Employment.objects.all()
        serializer = EmploymentSerializer(all_users, many=True)
        return Response(serializer.data,200)
    
    def post(self,request):
        serializer = EmploymentSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data,200)

class Hobbies(APIView,IsAuthenticated):
    serializer_class = HobbySerializer
    
    def get(self, request):
        all_user = Hobby.objects.all()
        serializer = HobbySerializer(all_user,many=True)
        return Response(serializer.data, 200)
    
    def post(self,request):
        serializer = HobbySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data,200)