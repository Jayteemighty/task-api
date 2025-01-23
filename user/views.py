from django.shortcuts import render
import os
import requests
from pathlib import Path
from django.shortcuts import redirect, render
from django.contrib.auth import get_user_model
from django.conf import settings
from rest_framework.views import APIView
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.parsers import MultiPartParser
from rest_framework.authtoken.models import Token

from . import serializers

User = get_user_model()

class RegisterView(generics.GenericAPIView):
    '''View to register users'''

    serializer_class = serializers.CreateAccountSerializer
    parser_classes = [MultiPartParser]
    permission_classes = [AllowAny]
    queryset = User.objects.all()
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class LoginView(generics.GenericAPIView):
    '''View to login users'''
    
    serializer_class = serializers.LoginSerializer
    permission_classes = []
    authentication_classes = []
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)

class UserDetailsView(generics.RetrieveUpdateAPIView):
    '''View to get, and update user account'''
    
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.UserDetailsSerializer
    
    def get_object(self):
        return self.request.user

class LogoutView(APIView):
    ''' View to logout users'''
    
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        current_user = request.user
        current_user_token = Token.objects.get(user=current_user)
        current_user_token.delete()
        
        return Response({'message': 'Logged out successfully'}, status=status.HTTP_200_OK)

class DeleteAccountView(APIView):
    '''View to delete a user's sccount. This will just make the user's account inactive.'''
    
    permission_classes = [IsAuthenticated]
    
    def delete(self, request):
        user = request.user
        user.is_active = False
        
        user.save()
        return Response({'message': 'Account deleted successfully'}, status=status.HTTP_200_OK)