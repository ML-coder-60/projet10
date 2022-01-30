from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from django.shortcuts import get_object_or_404

from authentication.serializers import CustomUserSerializer

from rest_framework import generics, status, mixins, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from api.permissions import CanUpdateDeleteProject, \
                            CheckContributor, \
                            CanCreateDeleteContributor, \
                            CanUpdateDeleteIssue, \
                            CanUpdateDeleteComment

from rest_framework_simplejwt.views import TokenObtainPairView

from api.models import Projects, Contributors, Issues, Comments
from authentication.models import CustomUser

from api.serializers import ProjectsDetailSerializer, ProjectsListSerializer, ContributorsDetailSerializer, \
                            ContributorsListSerializer, IssuesDetailSerializer, IssuesListSerializer,\
                            CommentsSerializer, CustomTokenObtainPairSerializer

from django.db.models import Q


class MultipleSerializerMixin():
    detail_serializer_class = None

    def get_serializer_class(self):
        if self.action == 'retrieve' and self.detail_serializer_class is not None:
            return self.detail_serializer_class
        return super().get_serializer_class()


class UserAPIView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = (AllowAny,)

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'id': serializer.instance.id}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProjectViewset(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin, mixins.DestroyModelMixin, MultipleSerializerMixin,
                     viewsets.GenericViewSet):

    serializer_class = ProjectsListSerializer
    detail_serializer_class = ProjectsDetailSerializer

    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
            return all projects whitch
                contributors    =>  user = request.user.id
                issues          => author_id or assignee_id =request.user.id
                comments        => author_id  = request.user.id

        """

        id_projects = [x.project_id for x in Contributors.objects.filter(user_id=self.request.user.id)]
        projects = Projects.objects.filter(Q(id__in=id_projects))
        if projects.count() >= 1:
            return projects
        else:
            get_object_or_404(projects)

    def get_permissions(self):
        if self.action == 'update' or self.action == 'destroy':
            composed_perm = IsAuthenticated & CheckContributor & CanUpdateDeleteProject
            return [composed_perm()]

        return super().get_permissions()

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        contributor = {
            "role": 'Créateur',
            "permission": "Créateur",
            "project": Projects.objects.get(title=request.data['title']).id,
            "user": request.user.id
        }
        serializer = ContributorsViewset.serializer_class(data=contributor)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class IssuesViewset(MultipleSerializerMixin, ModelViewSet):

    serializer_class = IssuesListSerializer
    detail_serializer_class = IssuesDetailSerializer
    permission_classes = [IsAuthenticated, CheckContributor]

    def get_permissions(self):
        if self.action == 'update' or self.action == 'destroy':
            composed_perm = IsAuthenticated & CheckContributor & CanUpdateDeleteIssue
            return [composed_perm()]

        return super().get_permissions()

    def create(self, request, **kwargs):
        if request.data:
            request.data._mutable = True
        request.data['author'] = self.request.user.id
        request.data['project'] = self.kwargs['id_project']
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, **kwargs):
        issue = Issues.objects.get(id=self.kwargs['pk'])
        for key, value in request.data.items():
            if key == 'assignee':
                value = CustomUser.objects.get(id=value)
            setattr(issue, key, value)
        serializer = IssuesListSerializer(issue)
        issue.save()
        return Response(serializer.data)

    def get_queryset(self, **kwargs):
        issues = Issues.objects.filter(project_id=self.kwargs['id_project'])
        if issues.count() >= 1:
            return issues
        else:
            get_object_or_404(issues)


class CommentsViewset(ModelViewSet):

    serializer_class = CommentsSerializer
    permission_classes = [IsAuthenticated, CheckContributor]

    def get_permissions(self):
        if self.action == 'update' or self.action == 'destroy':
            composed_perm = IsAuthenticated & CheckContributor & CanUpdateDeleteComment
            return [composed_perm()]

        return super().get_permissions()

    def get_queryset(self, **kwargs):
        comments = Comments.objects.filter(issue_id=self.kwargs['id_issue'])
        if comments.count() >= 1:
            return comments
        else:
            get_object_or_404(comments)

    def create(self, request, **kwargs):
        if request.data:
            request.data._mutable = True
        request.data['author'] = self.request.user.id
        request.data['issue'] = self.kwargs['id_issue']
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, **kwargs):
        comment = Comments.objects.get(id=self.kwargs['pk'])
        for key, value in request.data.items():
            setattr(comment, key, value)
        serializer = CommentsSerializer(comment)
        comment.save()
        return Response(serializer.data)


class ContributorsViewset(MultipleSerializerMixin, ModelViewSet):

    serializer_class = ContributorsListSerializer
    detail_serializer_class = ContributorsDetailSerializer

    permission_classes = [IsAuthenticated, CheckContributor]

    def get_queryset(self, **kwargs):
        contributors = Contributors.objects.filter(project_id=self.kwargs['id_project'])
        if contributors.count() >= 1:
            return contributors
        else:
            get_object_or_404(contributors)

    def get_permissions(self):
        if self.action == 'destroy' or self.action == 'create':
            composed_perm = IsAuthenticated & CheckContributor & CanCreateDeleteContributor
            return [composed_perm()]

        return super().get_permissions()

    def create(self, request, **kwargs):
        if request.data:
            request.data._mutable = True
        request.data['project'] = self.kwargs['id_project']
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomTokenObtainPairView(TokenObtainPairView):
    # Replace the serializer with your custom
    serializer_class = CustomTokenObtainPairSerializer
