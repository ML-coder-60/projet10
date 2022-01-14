from django.db import models
from django.conf import settings


class Projects(models.Model):

    class Type(models.TextChoices):
        BACK_END = 'Back-end'
        FRONT_END = 'front-end'
        IOS = 'IOS'
        ANDROID = 'Android'

    title = models.CharField(max_length=50)
    description = models.CharField(max_length=255)
    type = models.CharField(max_length=15, choices=Type.choices)
    contributor = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through='Contributors',
        related_name='contributions'
    )

    class Meta:
        verbose_name = 'Projet'
        verbose_name_plural = 'Projets'

    def __str__(self):
        return self.title

class Issues(models.Model):

    class Priority(models.TextChoices):
        LOW = 'Faible'
        MEDIUM = 'Moyenne'
        HIGH = 'Haute'

    class Status(models.TextChoices):
        TO_DO = 'A faire'
        IN_PROGESS = 'En cours'
        FINISHED = 'Terminé'

    class Tag(models.TextChoices):
        INCIDENT = 'bug'
        TICKET = 'tâche'
        CHANGE = 'amélioration'

    title = models.CharField(max_length=50)
    desc = models.CharField(max_length=255)
    tag = models.CharField(max_length=20,choices=Tag.choices, default='amélioration')
    priority = models.CharField(max_length=20, choices=Priority.choices, default='Faible')
    project =  models.ForeignKey(to=Projects, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=Status.choices, default='A faire')
    created_time = models.DateTimeField()
    author = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='authors')
    assignee = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Problème'
        verbose_name_plural = 'Problèmes'

    def __str__(self):
        return self.title

class Comments(models.Model):

    description = models.TextField(max_length=255)
    created_time = models.DateTimeField(auto_now_add=True)

    author =  models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    issue = models.ForeignKey(to=Issues, on_delete=models.CASCADE )

    class Meta:
        verbose_name = 'Commentaire'
        verbose_name_plural = 'Commentaires'

    def __str__(self):
        return self.description

class Contributors(models.Model):
    class Permission(models.TextChoices):
        ALL = 'Créateur'
        RESTRICTED = 'Restreint'

    class Role(models.TextChoices):
        CREATOR = 'Créateur'
        COLLABORATOR = 'Collaborateur'

    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    project = models.ForeignKey(to=Projects, on_delete=models.CASCADE)
    permission = models.CharField(max_length=250, choices=Permission.choices, default='Restreint')
    role =  models.CharField(max_length=20, choices=Role.choices, default='Collaborateur')


    def __str__(self):
        return self.user.email



    class Meta:
        unique_together = ('user','project')
        verbose_name = 'collaborateur'
        verbose_name_plural = 'collaborateurs'
