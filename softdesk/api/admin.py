from django.contrib import admin

from api.models import Projects, Issues, Comments, Contributors

class ContributorAdmin(admin.ModelAdmin):
    list_display = ('contributor','role','project')

admin.site.register(Contributors,ContributorAdmin)

class CommentsAdmin(admin.ModelAdmin):
    list_display = ('description','author','issue')

admin.site.register(Comments,CommentsAdmin)


class IssuesAdmin(admin.ModelAdmin):
    list_display = ('title','project','priority','status')

admin.site.register(Issues,IssuesAdmin)


class ProjectsAdmin(admin.ModelAdmin):
    list_display = ('title','type','author')

admin.site.register(Projects,ProjectsAdmin)