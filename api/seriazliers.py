from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from .models import Direction, Discipline, Student, Group, CustomUser


class RegistrationSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(max_length=256, write_only=True)
    user_type = serializers.CharField(max_length=256, write_only=True)

    class Meta:
        model = CustomUser
        fields = ['email', 'username', 'password', 'confirm_password', 'user_type']
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, attrs):
        confirm_password = attrs.pop('confirm_password')
        permissions = ['admin', 'curator']
        if not attrs.get('user_type'):
            return serializers.ValidationError('User permission required')
        if attrs.get('user_type') not in permissions:
            raise serializers.ValidationError("Invalid user permission")
        if not attrs.get('username'):
            raise serializers.ValidationError("Username required")
        if not attrs.get('email'):
            raise serializers.ValidationError("Email required")
        if not attrs.get('password') or not confirm_password:
            raise serializers.ValidationError("Password and confirm password required")
        if attrs.get('password') != confirm_password:
            raise serializers.ValidationError("Passwords missmatch")
        return attrs

    def create(self, validated_data):
        validated_data['is_staff'] = True if validated_data.get('user_type') == "admin" else False
        validated_data['is_curator'] = True if validated_data.get('user_type') == "curator" else False
        validated_data['password'] = make_password(validated_data.get('password'))
        validated_data.pop('user_type')
        return CustomUser.objects.create(**validated_data)


class LoginSerializer(serializers.Serializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'password']


class DirectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Direction
        fields = "__all__"


class DisciplineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discipline
        fields = "__all__"


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = "__all__"

    def create(self, validated_data):
        count_of_students = Student.objects.select_related('group').filter(group=validated_data.get('group')).count()
        if count_of_students > 20:
            raise serializers.ValidationError("Group is full")
        user = Student.objects.create(**validated_data)
        return user


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = "__all__"

