from rest_framework import serializers
from .models import Repository, Commit

class CommitSerializer(serializers.ModelSerializer):

    class Meta:
        model = Commit
        fields = (
            'sha', 'url', 'author', 'message', 'created_at',
        )

class RepositorySerializer(serializers.ModelSerializer):
    commits = CommitSerializer(source='commit_set', many=True, required=False)

    class Meta:
        model = Repository
        fields = (
            'name', 'full_name', 'description', 'commits',
        )
        read_only_fields = ('fullname', 'description', 'commits',)
