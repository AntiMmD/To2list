from django.db import models
from django.utils.timezone import now
from user.models import User
from django.core.exceptions import ValidationError


class Project(models.Model):
    ICON_CHOICES = (
        ('📁', 'Folder'),
        ('📋', 'Clipboard'),
        ('🎯', 'Target'),
        ('💡', 'Idea'),
        ('🏠', 'Home'),
        ('💼', 'Work'),
        ('📚', 'Study'),
        ('✨', 'Spark'),
        ('🌱', 'Growth'),
        ('⚡', 'Energy'),
    )

    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=8, choices=ICON_CHOICES, default='📋')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projects')
    date_created = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return f'{self.icon} {self.name}'

    @property
    def task_count(self):
        return self.tasks.count()

    @property
    def done_count(self):
        return self.tasks.filter(status='D').count()


class Task(models.Model):
    status_choices = (('P', 'Pending'), ('D', 'Done'))
    priority_choices = (
        ('U', 'Urgent'),
        ('I', 'Important'),
        ('IU', 'Important and urgent'),
        ('C', 'Casual'),
    )

    name = models.CharField(max_length=80)
    priority = models.CharField(max_length=2, choices=priority_choices, default='C')
    description = models.TextField(blank=True)
    date_created = models.DateTimeField(auto_now_add=True, editable=False)
    expiration_date = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=1, choices=status_choices, default='P')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='tasks',
        null=True,
        blank=True,
    )

    class Meta:
        ordering = ['expiration_date']

    def clean(self):
        if self.expiration_date and self.date_created:
            if self.expiration_date <= self.date_created:
                raise ValidationError({
                    'expiration_date': 'Expiration date must be after the creation date.'
                })

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
