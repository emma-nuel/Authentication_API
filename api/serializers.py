from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth import authenticate

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'phone_number', 'first_name', 'last_name', 'gender', 'age')
        extra_kwargs = {
            'password': {'required': True}
        }

class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = "__all__"

    def validate(self, attrs):
        username = attrs.get('username', '')
        if CustomUser.objects.filter(username=username).exists():
            raise serializers.ValidationError("Sorry Username Already Exists")
        return attrs
    
    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user
    
class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('phone_number', 'first_name', 'last_name', 'gender', 'age', 'password')

    def update(self, instance, validated_data):
        print(f"Data: {validated_data}")
        password = validated_data.pop('password')
        print(f"Password: {password}")
        if password:
            instance.set_password(password)
        instance = super().update(instance, validated_data)
        return instance
    
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(style={'input_type': 'password'}, trim_whitespace=False)

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if not username or not password:
            raise serializers.ValidationError("Please give both username and password.")

        if not CustomUser.objects.filter(username=username).exists():
            raise serializers.ValidationError('Username does not exist.')

        user = authenticate(request=self.context.get('request'), username=username,
                            password=password)
        print('User: ', user)
        if not user:
            raise serializers.ValidationError("Wrong Credentials.")

        attrs['user'] = user
        return attrs