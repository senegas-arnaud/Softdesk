from rest_framework import generics, permissions, status, filters
from rest_framework.response import Response
from .models import Project, Contributor, Issue, Comment
from .serializers import ProjectSerializer, ContributorSerializer, IssueSerializer, CommentSerializer
from rest_framework.exceptions import NotFound
from django_filters.rest_framework import DjangoFilterBackend


class ProjectListCreateView(generics.ListCreateAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['type']

    def get_queryset(self):
        return Project.objects.filter(contributors__user=self.request.user)

    def perform_create(self, serializer):
        project = serializer.save(author=self.request.user)
        Contributor.objects.create(user=self.request.user, project=project)


class ProjectDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Project.objects.filter(contributors__user=self.request.user)

    def update(self, request, *args, **kwargs):
        project = self.get_object()
        if project.author != request.user:
            return Response({"detail": "Vous n'êtes pas l'auteur de ce projet."}, status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        project = self.get_object()
        if project.author != request.user:
            return Response({"detail": "Vous n'êtes pas l'auteur de ce projet."}, status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)
    
    
class ContributorListCreateView(generics.ListCreateAPIView):
    serializer_class = ContributorSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Contributor.objects.filter(project_id=self.kwargs['project_pk'])

    def perform_create(self, serializer):
        project = Project.objects.get(pk=self.kwargs['project_pk'])
        if project.author != self.request.user:
            raise permissions.PermissionDenied("Seul l'auteur peut ajouter des contributeurs.")
        serializer.save(project=project)


class ContributorDestroyView(generics.DestroyAPIView):
    serializer_class = ContributorSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Contributor.objects.filter(project_id=self.kwargs['project_pk'])

    def destroy(self, request, *args, **kwargs):
        project = Project.objects.get(pk=self.kwargs['project_pk'])
        if project.author != request.user:
            raise permissions.PermissionDenied("Seul l'auteur peut supprimer des contributeurs.")
        return super().destroy(request, *args, **kwargs)


class IssueListCreateView(generics.ListCreateAPIView):
    serializer_class = IssueSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['priority', 'status', 'tag']

    def get_queryset(self):
        project = Project.objects.filter(
            pk=self.kwargs['project_pk'],
            contributors__user=self.request.user
        ).first()
        if not project:
            raise NotFound("Projet introuvable ou accès non autorisé.")
        return Issue.objects.filter(project=project)

    def perform_create(self, serializer):
        project = Project.objects.filter(
            pk=self.kwargs['project_pk'],
            contributors__user=self.request.user
        ).first()
        if not project:
            raise NotFound("Projet introuvable ou accès non autorisé.")
        serializer.save(author=self.request.user, project=project)


class IssueDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = IssueSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        project = Project.objects.filter(
            pk=self.kwargs['project_pk'],
            contributors__user=self.request.user
        ).first()
        if not project:
            raise NotFound("Projet introuvable ou accès non autorisé.")
        return Issue.objects.filter(project=project)

    def update(self, request, *args, **kwargs):
        issue = self.get_object()
        if issue.author != request.user:
            return Response({"detail": "Vous n'êtes pas l'auteur de cette issue."}, status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        issue = self.get_object()
        if issue.author != request.user:
            return Response({"detail": "Vous n'êtes pas l'auteur de cette issue."}, status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)


class CommentListCreateView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        project = Project.objects.filter(
            pk=self.kwargs['project_pk'],
            contributors__user=self.request.user
        ).first()
        if not project:
            raise NotFound("Projet introuvable ou accès non autorisé.")
        return Comment.objects.filter(issue_id=self.kwargs['issue_pk'])

    def perform_create(self, serializer):
        project = Project.objects.filter(
            pk=self.kwargs['project_pk'],
            contributors__user=self.request.user
        ).first()
        if not project:
            raise NotFound("Projet introuvable ou accès non autorisé.")
        issue = Issue.objects.get(pk=self.kwargs['issue_pk'])
        serializer.save(author=self.request.user, issue=issue)


class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        project = Project.objects.filter(
            pk=self.kwargs['project_pk'],
            contributors__user=self.request.user
        ).first()
        if not project:
            raise NotFound("Projet introuvable ou accès non autorisé.")
        return Comment.objects.filter(issue_id=self.kwargs['issue_pk'])

    def update(self, request, *args, **kwargs):
        comment = self.get_object()
        if comment.author != request.user:
            return Response({"detail": "Vous n'êtes pas l'auteur de ce commentaire."}, status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        comment = self.get_object()
        if comment.author != request.user:
            return Response({"detail": "Vous n'êtes pas l'auteur de ce commentaire."}, status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)