from django.shortcuts import render
from django.db.models import Subquery
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import Author, Inbox, Follow
from .serializers import AuthorSerializer
from django.contrib.auth import authenticate, login
import json
import datetime

class index(APIView):
    pass

class profile(APIView):
    pass

class followers(APIView):
    def get(self, request, author_id):
        follower_ids = Follow.objects.filter(toAuthor=author_id)
        follower_profiles = Author.objects.filter(authorID__in=follower_ids.values_list('fromAuthor', flat=True))
        serializer = AuthorSerializer(follower_profiles, many=True)
        response = {'type': 'followers', 'items': serializer.data}
        return Response(response)

class follower(APIView):
    authentication_classes = [BasicAuthentication]
    #permission_classes = [IsAuthenticated]

    def get(self, request, author_id, foreign_author_id):
        follower = Follow.objects.filter(toAuthor=author_id, fromAuthor=foreign_author_id)
        if not follower:
            return Response(status=404)
        else:
            return Response(status=200)

    def put(self, request, author_id, foreign_author_id):
        if request.user.is_authenticated:
            try:
                author = request.user.author
            except:
                # The user does not have an author profile
                return Response(status=403)
            if str(author.authorID) != author_id and str(author.authorID) != foreign_author_id:
                # The request was not made by the follower or author being followed
                return Response(status=403)
            try:
                toAuthor = Author.objects.get(authorID=author_id)
                fromAuthor = Author.objects.get(authorID=foreign_author_id)
            except:
                # One or both of the others do not exist
                return Response(status=404)
            # Add the follower
            follow, created = Follow.objects.get_or_create(fromAuthor=fromAuthor, toAuthor=toAuthor, defaults={'date': datetime.datetime.now()})
            follow.save()
            return Response(status=200)
        else:
            # Request was not authenticated
            return Response(status=401)

    def delete(self, request, author_id, foreign_author_id):
        if request.user.is_authenticated:
            try:
                author = request.user.author
            except:
                # The user does not have an author profile
                return Response(status=403)
            if str(author.authorID) != author_id and str(author.authorID) != foreign_author_id:
                # The request was not made by the follower or author being followed
                return Response(status=403)
            try:
                Follow.objects.get(fromAuthor=foreign_author_id, toAuthor=author_id).delete()
            except:
                # Nothing to delete
                return Response(status=404)
            return Response(status=200)
        else:
            # Request was not authenticated
            return Response(status=401)

class liked(APIView):
    pass

class inbox(APIView):
    pass