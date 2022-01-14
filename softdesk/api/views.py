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
                            UsersListSerializer

from django.db.models import Q

from icecream import ic

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

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return  self.detail_serializer_class
        return super().get_serializer_class()

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        project = Projects.objects.filter(title=request.data['title'])[0]

        Contributors.objects.create(
            role="Créateur",
            permission= "Créateur",
            project= project,
            user=self.request.user)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    #@action(methods=['get'], detail=True, permission_classes=[IsAuthenticated,])
    #def users(self, request, pk=None):
    #    #user = ContributorViewset(request).get_queryset()
    #    contribs = Contributors.objects.filter(project_id=pk)
    #    serializer =  ContributorsListSerializer(contribs, many=True)
    #    #headers = self.get_success_headers(user.data)
    #    #return Response(serializer.data, status=status.HTTP_200_OK, headers=headers)
    #    #return Response([contrib.permission for contrib in contribs])
    #    return Response(serializer.data)

class ContributorsViewset(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet):

    serializer_class = ContributorsListSerializer
    detail_serializer_class = ContributorsDetailSerializer

    permission_classes = [IsAuthenticated, ]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return  self.detail_serializer_class
        return super().get_serializer_class()


    def get_queryset(self, **kwargs):
        print(self.kwargs)
        return Contributors.objects.filter(project_id=self.kwargs['id_project'])

#class UsersViewset(mixins.CreateModelMixin,
#    mixins.ListModelMixin,
#    mixins.RetrieveModelMixin,
#    mixins.DestroyModelMixin,
#    viewsets.GenericViewSet):

#    serializer_class = UsersSerializer
#    permission_classes = [IsAuthenticated, ]

#    def get_queryset(self):
#        return CustomUser.objects.all()

class IssuesViewset(ModelViewSet):

    serializer_class = IssuesListSerializer
    detail_serializer_class = IssuesDetailSerializer
    permission_classes = [IsAuthenticated, ]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return  self.detail_serializer_class
        return super().get_serializer_class()

    def get_queryset(self):
        return Issues.objects.all()