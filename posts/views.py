from django.shortcuts import render
from rest_framework import generics, permissions, mixins, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from posts.models import Post, Vote
from posts.serializers import PostSerializer, VoteSerializer


class PostList(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(poster=self.request.user)


class PostRetrieveDestroy(generics.RetrieveDestroyAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        pk = self.kwargs['pk']
        post = Post.objects.filter(id=pk, poster=self.request.user)
        print(pk)
        print(self.request.user)
        return post

    def delete(self, request, *args, **kwargs):
        if self.get_queryset().exists():
            return self.destroy(request, *args, **kwargs)
        else:
            raise ValidationError("Either this post belongs to another user or it doesn't exist.")


class VoteList(generics.ListAPIView):
    serializer_class = VoteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Vote.objects.filter(user=self.request.user)


class VoteCreate(generics.ListCreateAPIView):
    serializer_class = VoteSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        pk = self.kwargs['pk']
        user = self.request.user
        post = Post.objects.get(pk=pk)
        return Vote.objects.filter(user=user, post=post)

    def perform_create(self, serializer):
        if self.get_queryset().exists():
            raise ValidationError("You've already voted the post.")
        pk = self.kwargs['pk']
        user = self.request.user
        post = Post.objects.get(pk=pk)
        serializer.save(user=user, post=post)

    def delete(self, request, *args, **kwargs):
        if self.get_queryset().exists():
            self.get_queryset().delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            raise ValidationError("You didn't vote this post before.")
