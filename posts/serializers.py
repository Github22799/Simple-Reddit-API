from rest_framework import serializers
from .models import Post, Vote


class PostSerializer(serializers.ModelSerializer):
    poster = serializers.ReadOnlyField(source='poster.username')
    poster_id = serializers.ReadOnlyField(source='poster.id')
    votes = serializers.SerializerMethodField()

    def get_votes(self, post):
        return Vote.objects.filter(post=post).count()

    class Meta:
        model = Post
        fields = ['title', 'poster', 'url', 'votes', 'created_time', 'id', 'poster_id']


class VoteSerializer(serializers.ModelSerializer):
    post_title = serializers.ReadOnlyField(source='post.title')

    class Meta:
        model = Vote
        fields = ['id', 'post', 'post_title']
