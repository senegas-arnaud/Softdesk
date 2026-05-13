from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from users.views import RegisterView, UserDetailView, LogoutView
from projects.views import ProjectListCreateView, ProjectDetailView, ContributorListCreateView, ContributorDestroyView, IssueListCreateView, IssueDetailView,CommentListCreateView,CommentDetailView
from drf_spectacular.views import SpectacularAPIView


urlpatterns = [
    path('admin/', admin.site.urls),
    # Users
    path('api/users/register/', RegisterView.as_view(), name='register'),
    path('api/users/login/', TokenObtainPairView.as_view(), name='login'),
    path('api/users/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/users/me/', UserDetailView.as_view(), name='user-detail'),
    path('api/users/logout/', LogoutView.as_view(), name='logout'),
    # Projects
    path('api/projects/', ProjectListCreateView.as_view(), name='project-list-create'),
    path('api/projects/<int:pk>/', ProjectDetailView.as_view(), name='project-detail'),
    # Contributors
    path('api/projects/<int:project_pk>/contributors/', ContributorListCreateView.as_view(), name='contributor-list-create'),
    path('api/projects/<int:project_pk>/contributors/<int:pk>/', ContributorDestroyView.as_view(), name='contributor-destroy'),
    # Issues
    path('api/projects/<int:project_pk>/issues/', IssueListCreateView.as_view(), name='issue-list-create'),
    path('api/projects/<int:project_pk>/issues/<int:pk>/', IssueDetailView.as_view(), name='issue-detail'),
    # Comments
    path('api/projects/<int:project_pk>/issues/<int:issue_pk>/comments/', CommentListCreateView.as_view(), name='comment-list-create'),
    path('api/projects/<int:project_pk>/issues/<int:issue_pk>/comments/<uuid:pk>/', CommentDetailView.as_view(), name='comment-detail'),
    # Doc
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
]