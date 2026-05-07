from rest_framework import serializers
from .models import Project, Contributor, Issue, Comment


class ProjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'type', 'author', 'created_time']
        read_only_fields = ['author', 'created_time']


class ContributorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Contributor
        fields = ['id', 'user', 'project', 'created_time']
        read_only_fields = ['created_time']


class IssueSerializer(serializers.ModelSerializer):

    class Meta:
        model = Issue
        fields = ['id', 'title', 'description', 'priority', 'tag', 'status', 'project', 'author', 'assigned_to', 'created_time']
        read_only_fields = ['author', 'created_time', 'project']

    def validate_assigned_to(self, value):
        request = self.context.get('request')
        project_pk = self.context.get('view').kwargs.get('project_pk')
        
        if value is not None:
            is_contributor = Contributor.objects.filter(
                user=value,
                project_id=project_pk
            ).exists()
            
            if not is_contributor:
                raise serializers.ValidationError(
                    "L'utilisateur assigné doit être contributeur du projet."
                )
        return value


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ['id', 'description', 'author', 'issue', 'created_time']
        read_only_fields = ['id', 'author', 'created_time', 'issue']