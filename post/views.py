import re
from django.shortcuts import render
from django.db.models import Subquery
from django.http import HttpResponse, JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Post, Like, Comment
from .serializers import PostSerializer, LikeSerializer, CommentSerializer
from author.models import Author, Follow, Inbox
from server.models import Node
import json
import requests
from django.core.paginator import InvalidPage, Paginator
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated
import uuid
from datetime import datetime, timezone
from django.contrib.contenttypes.models import ContentType
from Social_Distribution import utils

class index(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self,request,author_id):
        utils.update_authors()
        if not Author.objects.filter(authorID=author_id).exists:
            return Response("The author does not exist", status = 404)
        try:
            author = request.user.author
            if str(author.authorID) == author_id:
                # Get all posts for the author
                post_ids = Post.objects.filter(ownerID=author_id)
            else:
                # The user does not have an author profile
                # only get the public and listed posts
                post_ids = Post.objects.filter(ownerID=author_id, isPublic=True, isListed=True).order_by("-date")
        except Exception as e:
            print(e)
            # The user does not have an author profile
            # only get the public and listed posts
            post_ids = Post.objects.filter(ownerID=author_id, isPublic=True, isListed=True).order_by("-date")
        #if not post_ids:
        #    return {'type':'posts','page':page, 'size':size, 'items': []}
        try:
            size = int(request.query_params.get("size",5)) #5 is default right?
            page = int(request.query_params.get("page",1)) #By default, 1 object per page.
            paginator = Paginator(post_ids, size)
        except:
            return Response("Bad request. Invalid size or page parameters.", status=400)
        # create a paginator
        try :
            serializer = PostSerializer(paginator.page(page), many=True)
            pageData = serializer.data
        except InvalidPage:
            pageData = []
        response = {'type':'posts','page':page, 'size':size, 'items': pageData}
        return Response(response)

    # create a post and generate id
    def post(self,request,author_id):
        try:
            author = request.user.author
        except:
            # The user does not have an author profile
            return Response(status=403)
        if str(author.authorID) != author_id:
            # The request was made by a different author
            return Response(status=403)
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            post = serializer.save()
            # Send friend posts to all followers
            if post.isListed and not post.isPublic:
                follows = Follow.objects.filter(toAuthor=author_id)
                for follow in follows:
                    recipient = follow.fromAuthor
                    if recipient.node is not None:
                        # send the post to the foreign node
                        if recipient.node.host_url == "https://social-distribution-fall2021.herokuapp.com/api/":
                            destination = recipient.node.host_url + "author/" + str(recipient.authorID) + "/inbox"
                        else:
                            destination = recipient.node.host_url + "author/" + str(recipient.authorID) + "/inbox/"
                        serializer = PostSerializer(post)
                        response = requests.post(destination, auth=(recipient.node.username, recipient.node.password), json=serializer.data)
                        if response.status_code >= 300:
                            return Response(response.text, status=response.status_code)
                    else:
                        # send the post to the inbox on the local node
                        Inbox.objects.create(authorID=follow.fromAuthor, inboxType="post", fromAuthor=request.user.author, date=post.date, objectID=post.postID, content_type=ContentType.objects.get(model="post"))
            return Response(serializer.data, status=201)
        else:
            print(serializer.errors)
            return Response(status=400)

class comments(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, author_id, post_id):
        try:
            post = Post.objects.get(postID=post_id, ownerID=author_id)
            # post_comments = Comment.objects.filter(postID=post_id).order_by("-date")
        except Exception as e:
            print(e)
            return Response("The requested post does not exist.", status=404)
        postAuthor = Author.objects.get(authorID = author_id)
        if not post.isPublic:
            # only the author of the post can view the comments if the post is not public
            if postAuthor.node is not None:
                # author is from a different node
                return Response("This post's comments are private.", status=403)
            try:
                author = request.user.author
            except:
                # The user does not have an author profile
                return Response("This post's comments are private.", status=403)
            if str(author.authorID) != author_id:
                # The request was made by a different author
                return Response("This post's comments are private.", status=403)
        if postAuthor.node is not None:
            # Get the comments from a different node
            try:    
                size = int(request.query_params.get("size", 5))
                page = int(request.query_params.get("page", 1))
            except:
                return Response("Bad request. Invalid size or page parameters.", status=400)
            if postAuthor.node.host_url == "https://social-distribution-fall2021.herokuapp.com/api/":
                response = requests.get(postAuthor.node.host_url + "author/" + author_id + "/posts/" + post_id + "/comments", params={"page": page, "size": size})
            else:
                response = requests.get(postAuthor.node.host_url + "author/" + author_id + "/posts/" + post_id + "/comments/", params={"page": page, "size": size})
            print("foreign comments")
            print(response.text)
            print(response.status_code)
            if response.status_code >= 300:
                return Response(response.text, status=response.status_code)
            return Response(response.json())
        post_comments = Comment.objects.filter(postID=post_id).order_by("-date")
        try:    
            size = int(request.query_params.get("size", 5))
            page = int(request.query_params.get("page", 1))
            paginator = Paginator(post_comments, size)
            comment_serializer = CommentSerializer(paginator.get_page(page), many=True)
        except:
            return Response("Bad request. Invalid size or page parameters.", status=400)
        url = request.build_absolute_uri('')
        post_url = url[:-len("/comments")]
        response = {"type": "comments", "page": page, "size": size, "post": post_url, "id": url, "comments": comment_serializer.data}
        return Response(response, status=200)

    def post(self,request,author_id,post_id):
        try:
            post = Post.objects.get(postID=post_id, ownerID=author_id)
        except Post.DoesNotExist:
            return Response("The requested post does not exist.", status=404)
        postAuthor = Author.objects.get(authorID=author_id)
        # only post comments to public posts unless you own the post or follow the owner of the post
        if not post.isPublic:
            try:
                user = request.user.author
            except:
                # The user does not have an author profile
                return Response("You do not have permission to comment on this post.", status=403)
            if postAuthor.node is not None:
                # Check other node to see if user is following this author
                try:
                    response = requests.get(postAuthor.node.host_url + "author/" + author_id + "/followers", auth=(postAuthor.node.username, postAuthor.node.password))
                    is_author_friend = False
                    followers = response.json()["items"]
                    for follower in followers:
                        if follower["id"].split("/")[-1] == str(user.authorID):
                            is_author_friend = True
                except KeyError:
                    return Response("Unable to confirm that you have permission to view this post.", status = 403)
            else:
                # Check the local inbox to see if the user is following this author
                is_author_friend = Follow.objects.filter(toAuthor=author_id, fromAuthor=str(user.authorID)).exists()
            if not is_author_friend and str(user.authorID) != author_id:
                return Response("You do not have permission to comment on this post.", status = 403)
        # Create the comment
        data = request.data
        if data["contentType"] == "Text":
            data["contentType"] = "text/plain"
        comment_serializer = CommentSerializer(data=request.data, context={"post_id": post_id})
        if comment_serializer.is_valid():
            comment = comment_serializer.save()
        else:
            return Response("Malformed request.", status=400)
        # Send the comment to the post's author's inbox
        comment_serializer = CommentSerializer(comment)
        if postAuthor.node is not None:
            # Send to a different node
            if postAuthor.node.host_url == "https://social-distribution-fall2021.herokuapp.com/api/":
                response = requests.post(postAuthor.node.host_url + "author/" + author_id + "/inbox", auth=(postAuthor.node.username, postAuthor.node.password), json=comment_serializer.data)
            else:
                response = requests.post(postAuthor.node.host_url + "author/" + author_id + "/inbox/", auth=(postAuthor.node.username, postAuthor.node.password), json=comment_serializer.data)
            if response.status_code >= 300:
                return Response(response.text, response.status_code)
        else:
             Inbox.objects.create(authorID=postAuthor, inboxType="comment", fromAuthor=comment.authorID, date=comment.date, objectID=comment.commentID, content_type=ContentType.objects.get(model="comment"))
        return Response(comment_serializer.data, status=201)

class post(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    #permission_classes = [IsAuthenticated]

    def get(self,request,author_id, post_id):
        try:
            post = Post.objects.get(ownerID=author_id, postID=post_id)
        except Post.DoesNotExist:
            return Response("The requested post does not exist.", status = 404)
        # only return public post unless you own the post or follow the owner of the post
        if not post.isPublic:
            try:
                user = request.user.author
            except:
                # The user does not have an author profile
                return Response("You do not have permission to view this post.", status=403)
            postAuthor = Author.objects.get(authorID=author_id)
            if postAuthor.node is not None:
                # Check other node to see if user is following this author
                try:
                    response = requests.get(postAuthor.node.host_url + "author/" + author_id + "/followers", auth=(postAuthor.node.username, postAuthor.node.password))
                    is_author_friend = False
                    followers = response.json()["items"]
                    for follower in followers:
                        if follower["id"].split("/")[-1] == str(user.authorID):
                            is_author_friend = True
                except KeyError:
                    return Response("Unable to confirm that you have permission to view this post.", status = 403)
            else:
                # Check the local inbox to see if the user is following this author
                is_author_friend = Follow.objects.filter(toAuthor=author_id, fromAuthor=str(user.authorID)).exists()
            if not is_author_friend and str(user.authorID) != author_id:
                return Response("You do not have permission to view this post.", status = 403)
        serializer = PostSerializer(post)
        return Response(serializer.data, status=200)

    #update the post with postId in url
    def post(self,request,author_id,post_id):
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
                post = Post.objects.get(ownerID=author_id,postID=post_id)
                update_data = request.data
                serializer = PostSerializer(post,data=update_data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    # returns the updated post
                    return JsonResponse(serializer.data, status=201)
                return Response(status=422)
            except Post.DoesNotExist:
                return Response(status=404)
        else:
            return Response(status=401)

    #create a post with that id in the url
    def put(self,request,author_id,post_id):
        if request.user.is_authenticated:
            try:
                author = request.user.author
            except:
                # The user does not have an author profile
                return Response(status=403)
            if str(author.authorID) != author_id:
                # The request was made by a different author
                return Response(status=403)
            if Post.objects.filter(ownerID=author_id, postID = post_id).exists():
                return Response(status=409)
            post = Post.objects.create(ownerID=request.user.author, postID=post_id, date=datetime.now(timezone.utc).astimezone(), isPublic=True, isListed=True, hasImage=False)
            post.save()
            return Response(status=201)
        else:
            return Response(status=401)

    def delete(self,request,author_id,post_id):
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
                Post.objects.get(ownerID=author_id,postID=post_id).delete()
            except:
                return Response("No such post exists, Delete unsuccessful.",status=404)
            return Response(status=200)
        else:
            return Response(status=401)

class likes(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self,request,author_id,post_id):
        if not Post.objects.filter(postID=post_id, ownerID=author_id).exists():
            return Response(status=404)
        postAuthor = Author.objects.get(authorID = author_id)
        if postAuthor.node is not None:
            # Get the likes from a different node
            if postAuthor.node.host_url == "https://social-distribution-fall2021.herokuapp.com/api/":
                response = requests.get(postAuthor.node.host_url + "author/" + author_id + "/posts/" + post_id + "/likes", auth=(postAuthor.node.username, postAuthor.node.password))
            else:
                response = requests.get(postAuthor.node.host_url + "author/" + author_id + "/posts/" + post_id + "/likes/", auth=(postAuthor.node.username, postAuthor.node.password))
            if response.status_code >= 300:
                return Response(response.text, status=response.status_code)
            data = response.json()
            if isinstance(data, dict):
                return Response(data)
            elif isinstance(data, list):
                response = {'type':'likes','items': data}
                return Response(response)
        else:
            likes = Like.objects.filter(objectID=post_id)
            serializer = LikeSerializer(likes, many = True)
            response = {'type':'likes','items': serializer.data}
            return Response(response)

class commentLikes(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self,request,author_id,post_id,comment_id):
        #print("here")
        if not Post.objects.filter(postID=post_id, ownerID=author_id).exists() or not Comment.objects.filter(commentID=comment_id, postID=post_id).exists():
            #print("NOT FOUND")
            #if Post.objects.filter(postID=post_id, ownerID=author_id).exists():
                #print("post not found")
            #else:
                #print("comment not found")
            return Response("Not found", status=404)
        postAuthor = Author.objects.get(authorID = author_id)
        if postAuthor.node is not None:
            # Get the likes from a different node
            if postAuthor.node.host_url == "https://social-distribution-fall2021.herokuapp.com/api/":
                response = requests.get(postAuthor.node.host_url + "author/" + author_id + "/posts/" + post_id + "/comments" + comment_id, auth=(postAuthor.node.username, postAuthor.node.password))
            else:
                response = requests.get(postAuthor.node.host_url + "author/" + author_id + "/posts/" + post_id + "/comments/" + comment_id, auth=(postAuthor.node.username, postAuthor.node.password))
            if response.status_code >= 300:
                return Response(response.text, status=response.status_code)
            data = response.json()
            if isinstance(data, dict):
                return Response(data)
            elif isinstance(data, list):
                response = {'type':'likes','items': data}
                return Response(response)
        likes = Like.objects.filter(objectID=comment_id)
        serializer = LikeSerializer(likes,many = True)
        response = {'type':'likes','items': serializer.data}
        return Response(response)
