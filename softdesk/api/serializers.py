from rest_framework import serializers
from api.models import Projects, Contributors, Issues, Comments
from authentication.models import CustomUser
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.db.models import Q

class CommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = ['id', 'description', 'created_time', 'author', 'issue' ]

class IssuesDetailSerializer(serializers.ModelSerializer):
    comment = serializers.SerializerMethodField()
    class Meta:
        model = Issues
        fields = ['id',
                  'title',
                  'desc',
                  'tag',
                  'priority',
                  'status',
                  'created_time',
                  'assignee',
                  'author',
                  'project',
                  'comment'
                  ]

    def get_comment(self, instance):
        comment = Comments.objects.filter(issue_id=instance.id)
        serializer = CommentsSerializer(comment, many=True)
        return serializer.data

class IssuesListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issues
        fields = ['id',
                  'title',
                  'desc',
                  'tag',
                  'priority',
                  'status',
                  'created_time',
                  'assignee',
                  'author',
                  'project'
                  ]

class UsersDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id','email','first_name','last_name',]

class UsersListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email']


class ContributorsListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contributors
        fields = ['id','user', 'project', 'permission', 'role']
        read_only = ['permission', 'role']

    def validate(self, data):
        """ Check that there is only one creator per project """
        if 'Créateur' in data.values():
            if data['role'] == 'Créateur':
                if Contributors.objects.filter( Q(project=data['project']) & Q(role='Créateur')).exists():
                    raise serializers.ValidationError(
                        'A user with the creator role already exists for this project')
        return data


class ContributorsDetailSerializer(serializers.ModelSerializer):
    user = UsersDetailSerializer()
    class Meta:
        model = Contributors
        fields = ['id','user', 'project', 'permission', 'role']

class ProjectsListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Projects
        fields = ['id','title', 'description', 'type']

    def validate_title(self, value):
        # Nous vérifions que le projet existe
        if Projects.objects.filter(title=value).exists():
        # En cas d'erreur, DRF nous met à disposition l'exception ValidationError
            raise serializers.ValidationError('Projects already exists')
        return value

    def validate(self, data):
        if data['title'] not in data['description']:
            raise serializers.ValidationError('Name must be in description')
        return data


class ProjectsDetailSerializer(serializers.ModelSerializer):
    contributor =  serializers.SerializerMethodField()
    issue = serializers.SerializerMethodField()

    class Meta:
        model = Projects
        fields = ['id','title', 'description', 'type', 'contributor','issue']
        depth = 1

    def get_contributor(self, instance):
        contributor = Contributors.objects.filter(project_id=instance.id)
        serializer = ContributorsDetailSerializer(contributor, many=True)
        return serializer.data

    def get_issue(self, instance):
        issue = Issues.objects.filter(project_id=instance.id)
        serializer = IssuesDetailSerializer(issue, many=True)
        return serializer.data

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        # The default result (access/refresh tokens)
        data = super(CustomTokenObtainPairSerializer, self).validate(attrs)
        # Custom data you want to include
        data.update({'id': self.user.id})
        # and everything else you want to send in the response
        return data