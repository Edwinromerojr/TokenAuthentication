from django.shortcuts import render
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated

from .serializers import UserSerializer
# Create your views here.
@api_view(["POST"])
def signUp(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()

        user = User.objects.get(username=request.data['username'])
        token = Token.objects.get(user=user)

        serializer = UserSerializer(user)

        data = {
            "user": serializer.data,
            "token": token.key
        }

        return Response(data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["POST"])
def loginPage(request):
    data = request.data
    authenticate_user = authenticate(username=data['username'], password=data['password'])

    if authenticate_user is not None:
        user = User.objects.get(username=data['username'])
        serializer = UserSerializer(user)

        response_data = {
            'user': serializer.data,
        }

        token, created_token = Token.objects.get_or_create(user=user)
        
        if token:
            response_data['token'] = token.key
        elif created_token:
            response_data['token'] = created_token.key
        return Response(response_data)
    return Response({"detail": "not found"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def testView(request):
    return Response({"message": "test view page"})

@api_view(["GET"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def logoutUser(request):

    request.user.auth_token.delete()

    return Response({"message": "logout was successful"})