from rest_framework import serializers
from .models import Repository, Commit

class CommitSerializer(serializers.ModelSerializer):

    class Meta:
        model = Commit
        fields = (
            'url', 'author', 'commiter', 'message', 'description',
        )

class RepositorySerializer(serializers.ModelSerializer):
    commits = CommitSerializer(source='installment_set', many=True, required=False)

    class Meta:
        model = Repository
        fields = (
            'name', 'full_name', 'description', 'commits',
        )
        read_only_fields = ('fullname', 'description', 'commits',)
