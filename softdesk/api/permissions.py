from rest_framework import permissions
from api.models import Contributors, Issues, Comments
from django.db.models import Q


class CheckInteger():

    def check_int(self,data):
        try:
            return int(data)
        except ValueError:
            return False

class CheckContributor(permissions.BasePermission):
    """
        Check user is contributor project
    """
    message = "Vous n'êtes pas contributeur du projet"

    def has_permission(self, request, view):

        if 'id_project' in view.kwargs:
            project_id = view.kwargs['id_project']
        elif 'pk' in view.kwargs:
            project_id = view.kwargs['pk']
        else:
            return False
        if not CheckInteger().check_int(project_id):
            return False
        if Contributors.objects.filter(Q(project_id=project_id) & Q(user_id=request.user.id)).exists():
             return True


class CanUpdateDeleteProject(permissions.BasePermission):
    """
        Check that user has creator role

    """
    message = "Vous n'avez pas les droits pour cette action"

    def has_permission(self, request, view):
        if 'pk' in view.kwargs:
            project_id = view.kwargs['pk']
        else:
            return  False
        if not CheckInteger().check_int(project_id):
            return False

        if Contributors.objects.filter(
                Q(project_id=project_id) &
                Q(user_id=request.user.id) &
                Q(role='Créateur')).exists():

                return True
        return False


class CanCreateDeleteContributor(permissions.BasePermission):
    """
        Check that user has creator permissions
        checks that the contributor who is to be deleted is not an author
    """

    message = "Vous n'avez pas les droits pour cette action"

    def has_permission(self, request, view):
        if 'id_project' in view.kwargs:
            id_project = view.kwargs['id_project']
        else:
            return  False
        if not CheckInteger().check_int(id_project):
            return False

        if request.method == 'POST':
            if Contributors.objects.filter(
                Q(project_id=id_project) &
                Q(user_id=request.user.id) &
                Q(permission='Créateur')).exists():
                return True


        if request.method == 'DELETE':
            print(request.user.id)
            print(view.kwargs['pk'])
            if  Contributors.objects.filter(
                    Q(project_id=id_project) &
                    Q(user_id=request.user.id) &
                    Q(permission='Créateur')).exists() and \
                Contributors.objects.filter(
                    Q(id=view.kwargs['pk']) &
                    Q(role = 'Collaborateur')).exists():
                return True
        return False


class CanUpdateDeleteIssue(permissions.BasePermission):
    """
        Check that user is owner Issues
    """

    message = "Vous n'avez pas les droits pour cette action"

    def has_permission(self, request, view):
        if 'id_project' in view.kwargs and 'pk' in view.kwargs:
            id_project = view.kwargs['id_project']
            id_issue = view.kwargs['pk']
        else:
            return False

        if not CheckInteger().check_int(id_project) or not CheckInteger().check_int(id_issue):
            return False
        if Issues.objects.filter( Q(project_id=id_project) &
                                  Q(author_id=request.user.id) &
                                  Q(id=id_issue)).exists():
            return True
        return False


class CanUpdateDeleteComment(permissions.BasePermission):
    """
        Check that user is owner Comments
    """

    message = "Vous n'avez pas les droits pour cette action"


    def has_permission(self, request, view):
        if 'id_issue' in view.kwargs and 'pk' in view.kwargs:
            id_issue = view.kwargs['id_issue']
            id_comment = view.kwargs['pk']
        else:
            return False
        if CheckInteger().check_int(id_issue) or CheckInteger().check_int(id_comment):
            return False
        if Comments.objects.filter( Q(issue_id=id_issue) &
                                  Q(author_id=request.user.id) &
                                  Q(id=id_comment)).exists():
            return True
        return False
