from rest_framework import serializers
from api.models import Projects, Contributors, Issues, Comments
from authentication.models import CustomUser
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.db.models import Q

class CommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = ['id', 'description', 'author','issue', 'created_time']

class IssuesDetailSerializer(serializers.ModelSerializer):
    comment = serializers.SerializerMethodField()
    class Meta:
        model = Issues
        fields = ['id', 'title', 'desc', 'tag', 'priority',
                  'status', 'created_time', 'assignee',
                  'author', 'project', 'comment'
                  ]

    def get_comment(self, instance):
        comment = Comments.objects.filter(issue_id=instance.id)
        serializer = CommentsSerializer(comment, many=True)
        return serializer.data

class IssuesListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issues
        fields = ['id', 'title', 'desc', 'tag', 'priority',
                  'status', 'created_time', 'assignee',
                  'author', 'project'
                  ]

    def validate(self, data):
        if Projects.objects.filter(title=data['title'], description=data['desc']).exists():
            raise serializers.ValidationError('Projects already exists')
        if data['title'] not in data['desc']:
            raise serializers.ValidationError('Name must be in description')
        return data


class UsersDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id','first_name','last_name',]

class UsersListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id']


class ContributorsListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contributors
        fields = ['id','user', 'project', 'permission','role']

class ContributorsDetailSerializer(serializers.ModelSerializer):
    user = UsersDetailSerializer()
    class Meta:
        model = Contributors
        fields = ['id','user', 'project', 'permission', 'role']

class ProjectsListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Projects
        fields = ['id','title', 'description', 'type']

    def validate(self, data):
        if Projects.objects.filter(title=data['title'], description=data['description']).exists():
            raise serializers.ValidationError('Projects already exists')
        if data['title'] not in data['description']:
            raise serializers.ValidationError('Name must be in description')
        return data


class ProjectsDetailSerializer(serializers.ModelSerializer):
    contributor =  serializers.SerializerMethodField()
    issue = serializers.SerializerMethodField()

    class Meta:
        model = Projects
        fields = ['id','title', 'description', 'type', 'contributor','issue']

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