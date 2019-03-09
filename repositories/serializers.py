from rest_framework import serializers

from .models import Commit, Repository


class CommitSerializer(serializers.ModelSerializer):
    repository_name = serializers.StringRelatedField(source='repository', read_only=True)
    repository_id = serializers.PrimaryKeyRelatedField(source='repository', read_only=True)

    class Meta:
        model = Commit
        fields = (
            'sha', 'url', 'author', 'message', 'created_at',
            'repository_name', 'repository_id'
        )


class RepositorySerializer(serializers.ModelSerializer):
    commits = CommitSerializer(source='commit_set', many=True, required=False)

    class Meta:
        model = Repository
        fields = (
            'id', 'name', 'full_name', 'description', 'commits',
        )
        read_only_fields = ('id', 'fullname', 'description', 'commits',)
