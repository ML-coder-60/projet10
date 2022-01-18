from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet

from authentication.serializers import CustomUserSerializer

from rest_framework.decorators import action

from rest_framework import generics, status, mixins, viewsets
from rest_framework.permissions import IsAuthenticated,AllowAny

from api.models import Projects, Contributors, Issues, Comments
from authentication.models import CustomUser


from icecream import ic

from api.serializers import ProjectsDetailSerializer, \
                            ProjectsListSerializer, \
                            ContributorsDetailSerializer, \
                            ContributorsListSerializer, \
                            IssuesDetailSerializer, \
                            IssuesListSerializer,\
                            UsersDetailSerializer, \
                            UsersListSerializer, \
                            CommentsSerializer

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


class ProjectViewset(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    MultipleSerializerMixin,
    viewsets.GenericViewSet):

    serializer_class = ProjectsListSerializer
    detail_serializer_class = ProjectsDetailSerializer

    permission_classes = [IsAuthenticated, ]
    

    def get_queryset(self):
        """
            return all projects whitch
                contributors    =>  user = request.user.id
                issues          => author_id or assignee_id =request.user.id
                comments        => author_id  = request.user.id

        """

        #######  a vérifier ....
        id_contrib_projects = [x.project_id for x in Contributors.objects.filter(user_id=self.request.user.id)]
        id_issues_projects = [x.project_id for x in Issues.objects.filter(
            Q(author_id=self.request.user.id) | Q(assignee_id=self.request.user.id))]
        id_comments_projects =  [x.project_id for x in Issues.objects.filter(
                    id__in=[x.issue_id for x in Comments.objects.filter(author_id=self.request.user.id)])]
        projects = Projects.objects.filter(
            Q(id__in=id_contrib_projects) | Q(id__in=id_issues_projects) | Q(id__in=id_comments_projects)
        )
        return projects

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        contributor = {
            "role": 'Créateur',
            "permission": "Créateur",
            "project": Projects.objects.get(title=request.data['title']).id,
            "user": self.request.user.id
        }
        serializer = ContributorsViewset.serializer_class(data=contributor)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class IssuesViewset(ModelViewSet):

    serializer_class = IssuesDetailSerializer
    detail_serializer_class = IssuesDetailSerializer
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self, **kwargs):
        print('test')
        return Issues.objects.filter(project_id=self.kwargs['id_project'])

class CommentsViewset(ModelViewSet):

    serializer_class = CommentsSerializer
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self, **kwargs):
        return Comments.objects.filter(issue_id=self.kwargs['id_issue'])


class ContributorsViewset(MultipleSerializerMixin,ModelViewSet):
    serializer_class = ContributorsListSerializer
    detail_serializer_class = ContributorsDetailSerializer
    permission_classes = [IsAuthenticated, ]


    def get_queryset(self, **kwargs):
        return Contributors.objects.filter(project_id=self.kwargs['id_project'])

    def create(self, request, **kwargs):
        self.request.data._mutable = True
        self.request.data['project'] =  self.kwargs['id_project']
        serializer = ContributorsViewset.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
