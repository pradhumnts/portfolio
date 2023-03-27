from rest_framework import serializers
from .models import UserData, Employment, Hobby, Skills
from django.contrib.auth.models import User

from datetime import datetime, date

def get_age(birthdate):
    date_of_birth = datetime.strptime(birthdate.strftime("%Y-%m-%d"), "%Y-%m-%d")
    today = date.today()

    age = today.year - date_of_birth.year - ((today.month, today.day) < (date_of_birth.month, date_of_birth.day))
    return age

class EmploymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employment
        exclude = ["created_at", "updated_at", "user", "id"]
    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employment
        fields = '__all__'
    
class HobbySerializer(serializers.ModelSerializer):
    class Meta:
        model = Hobby
        fields = '__all__'


class UserDataSerializer(serializers.ModelSerializer):

    
    def to_representation(self, instance):
        # Call the parent `to_representation()` method to get the default representation
        representation = super().to_representation(instance)

        # Customize the representation
        # For example, convert a datetime field to a string in a specific format
        representation['created_at'] = instance.created_at.strftime('%Y-%m-%d %H:%M:%S')
        representation["profileViews"] = instance.profile_views
        representation["personalInfo"] = {
            "contact": instance.phone,
            "email": instance.user.email,
            "name": instance.user.first_name + ' ' + instance.user.last_name,
            "picture": "https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=774&q=80",
            "role": instance.role,
            "age": get_age(instance.date_of_birth),
            "location": "San Francisco, CA",
            "description": instance.description,
        }

        return representation

    skills = serializers.PrimaryKeyRelatedField(queryset=Skills.objects.all(), many=True)
    jobHistory = serializers.SerializerMethodField()

    email = serializers.EmailField(write_only=True)
    phone = serializers.CharField(write_only=True)
    photo = serializers.ImageField(write_only=True)
    role = serializers.CharField(write_only=True)
    date_of_birth = serializers.DateField(write_only=True)
    description = serializers.CharField(write_only=True)
    profile_views = serializers.IntegerField(write_only=True)

    class Meta:
        model = UserData
        depth = 1
        fields = "__all__"
        
    def get_jobHistory(self, object):
        jobs = Employment.objects.filter(user__id=object.user.id)
        serializers = EmploymentSerializer(jobs, many=True)
        return serializers.data

    def create(self, validated_data):
        skills = validated_data.pop('skills')
        user_data = UserData.objects.create(**validated_data)

        for skill_obj in skills:
            skill, created = Skills.objects.get_or_create(id=skill_obj.id)
            user_data.skills.add(skill)
            
        return user_data