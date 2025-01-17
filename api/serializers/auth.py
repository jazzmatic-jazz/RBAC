from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from api.models import User, Resource


class UserSerializer(ModelSerializer):
    password = serializers.CharField(max_length=20, write_only=True,  required=False, allow_null=True)
    confirm_password = serializers.CharField(max_length=20, write_only=True,  required=False, allow_null=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'name', 'role', 'password', 'confirm_password']

    def validate(self, attrs):
        print("valide")
        password = attrs.get('password')
        confirm_password = attrs.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            raise serializers.ValidationError("Password does not match")
        return attrs
    
    def create(self, validated_data):
        print("create")
        user = User(
            username = validated_data['username'],
            name = validated_data['name'],
            email = validated_data['email'],
            role = validated_data['role'],
        )

        user.set_password(validated_data['password'])
        user.save()
        return user
    
    def update(self, instance, validated_data):
        print("update")

        get_email = validated_data.get('email', instance.email)
        get_username = validated_data.get('username', instance.username)
        get_name = validated_data.get('name', instance.name)
        get_role = validated_data.get('role', instance.role)
        
        instance.email = get_email
        instance.name = get_name
        instance.username = get_username
        instance.role = get_role

        password = validated_data.get('password', None)
        validated_data.pop('confirm_password', None) 
        
        if password:
            instance.set_password(password)  
        instance.save()

        return instance