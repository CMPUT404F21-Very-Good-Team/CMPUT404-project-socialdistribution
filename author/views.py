from django.shortcuts import render
from django.db.models import Subquery
from django.http import HttpResponse, JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import JSONParser
from .models import Author, Inbox, Follow
from .serializers import AuthorSerializer, AuthorCreationSerializer
from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from django.contrib.auth.models import User

import json
from django.utils import timezone
from django.conf import settings



from author import serializers

class index(APIView):
    def post(self, request):
        author_data = JSONParser().parse(request)
        author_serializer = AuthorCreationSerializer(data=author_data)
        if author_serializer.is_valid():
            author_serializer.save()
            return JsonResponse(author_serializer.data, status=201)
        else:
            print(author_serializer.errors)
        return Response(status = 422)

class profile(APIView):
    def get(self, request, author_id):
        try:
            author_profile = Author.objects.get(authorID= author_id)
            serializer = AuthorSerializer(author_profile)
            return Response(serializer.data)
        except Author.DoesNotExist:
            return Response("This author does not exist",status=404)




class login(APIView):
    def post(self, request):
        try:
            username = request.POST['username']
            password = request.POST['password']
        except:
            return Response(status=400)
        user = authenticate(request=request, username=username, password=password)
        if user is not None:
            django_login(request, user)
            return Response(status=200)
        else:
            return Response(status=401)

class logout(APIView):
    def post(self, request):
        django_logout(request)
        return Response(status=200)

class register(APIView):
    def post(self, request):
        if not settings.ALLOW_USER_SIGN_UP:
            return Response(status=403)
        try:
            username = request.POST['username']
            password = request.POST['password']
        except:
            return Response(status=400)
        if User.objects.filter(username=username).exists():
            # The user already exists
            return Response(status=409)
        user = User.objects.create_user(username=username, password=password)
        user.is_active = False
        user.save()
        author = Author(user=user)
        author.save()
        return Response(status=201)
  

class followers(APIView):
    def get(self, request, author_id):
        try:
            author = Author.objects.get(authorID=author_id)
        except:
            # The author does not exist
            return Response(status=404)
        follower_ids = Follow.objects.filter(toAuthor=author_id)
        follower_profiles = Author.objects.filter(authorID__in=follower_ids.values_list('fromAuthor', flat=True))
        serializer = AuthorSerializer(follower_profiles, many=True)
        response = {'type': 'followers', 'items': serializer.data}
        return Response(response)


class follower(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    #permission_classes = [IsAuthenticated]

    def get(self, request, author_id, foreign_author_id):
        follower = Follow.objects.filter(toAuthor=author_id, fromAuthor=foreign_author_id)
        if not follower:
            return Response(status=404)
        else:
            return Response(status=200)

    def put(self, request, author_id, foreign_author_id):
        print("test")
        print(request.user)
        if request.user.is_authenticated:
            try:
                author = request.user.author
            except:
                # The user does not have an author profile
                return Response(status=403)
            if str(author.authorID) != author_id:
                # The request was made by a different author
                return Response(status=403)
            try:
                fromAuthor = Author.objects.get(authorID=foreign_author_id)
            except:
                # The foreign author does not exist
                return Response(status=404)
            if Follow.objects.filter(fromAuthor=fromAuthor, toAuthor=author).exists():
                # The follower already exists
                return Response(status=409)
            # Add the follower
            follow = Follow.objects.create(fromAuthor=fromAuthor, toAuthor=author, date=timezone.now())
            follow.save()
            return Response(status=201)
        else:
            # Request was not authenticated
            return Response(status=401)

    def delete(self, request, author_id, foreign_author_id):
        try:
            Follow.objects.get(fromAuthor=foreign_author_id, toAuthor=author_id).delete()
        except:
            # Nothing to delete
            return Response(status=404)
        return Response(status=200)

class liked(APIView):
    pass

class inbox(APIView):
    pass
