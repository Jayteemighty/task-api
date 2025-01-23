from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers, status
from rest_framework.authtoken.models import Token

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    '''Serializer to get and update a user's details.'''
    
    class Meta:
        model = User
        fields = ["id", "email", "first_name", "last_name", "date_of_birth", "age"]

class CreateAccountSerializer(serializers.ModelSerializer):
    ''' Serializer to create new user '''

    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'password2', 'first_name', 'last_name', 'date_of_birth', 'age']
        read_only_fields = ['id']        
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, data):
        '''Account creation validation function'''

        if data['password'] != data['password2']:
            raise serializers.ValidationError({'error': 'Your passwords do not match'}, code=status.HTTP_400_BAD_REQUEST)
        
        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError({'error': 'Email already exists'}, code=status.HTTP_400_BAD_REQUEST)
        
        validate_password(data['password'])
        
        return data
    
    def create(self, validated_data):
        '''Account creation function'''
        
        password = validated_data.get('password')
        validated_data.pop('password2')

        account = User.objects.create(**validated_data)
        account.set_password(raw_password=password)
        account.save()
        
        Token.objects.create(user=account)

        return account

class LoginSerializer(serializers.Serializer):
    '''Serializer to log in a user.'''

    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)
    
    def validate(self, data):
        '''Authentication validation function'''

        user = authenticate(email=data['email'], password=data['password'])

        if user is None:
            raise serializers.ValidationError({'error': 'Invalid credentials'}, code=status.HTTP_400_BAD_REQUEST)
        
        email = data.pop('email')
        data.pop('password')

        token = Token.objects.get_or_create(user=user)
        
        data['message'] = f'Welcome {email}'
        data['token'] = token[0].key

        return data


class UserDetailsSerializer(serializers.ModelSerializer):
    '''Serializer to get and update a user's details.'''

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', "date_of_birth", "age"]
        read_only_fields = ['id', 'email']        
    
    def update(self, instance, validated_data):
        '''Update details function'''

        for key, value in validated_data.items():
            setattr(instance, key, value)

        instance.save()

        return instance