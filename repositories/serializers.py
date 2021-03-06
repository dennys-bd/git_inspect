from rest_framework import serializers

from .models import Commit, Repository


class CommitSerializer(serializers.ModelSerializer):
    repository_name = serializers.StringRelatedField(source='repository', read_only=True)
    repository_id = serializers.PrimaryKeyRelatedField(source='repository', read_only=True)

    class Meta:
        model = Commit
        fields = (
            'sha', 'url', 'author', 'message', 'created',
            'repository_name', 'repository_id'
        )
        read_only_fields = ('sha', 'url', 'author',)


class RepositorySerializer(serializers.ModelSerializer):
    # commits = CommitSerializer(source='commit_set', many=True, required=False)

    class Meta:
        model = Repository
        fields = (
            'id', 'name', 'full_name', 'description', 'github_hook_id'
        )
        read_only_fields = ('id', 'fullname', 'description', 'github_hook_id',)
