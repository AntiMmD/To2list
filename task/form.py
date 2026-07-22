from django import forms
from task.models import Task, Project


class CreateTask(forms.ModelForm):
    class Meta:
        model = Task
        fields = '__all__'
        exclude = ['date_created', 'status', 'user', 'project']
        widgets = {
            'expiration_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Optional notes…'}),
            'name': forms.TextInput(attrs={'placeholder': 'Task name'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['description'].required = False
        self.fields['expiration_date'].required = False
        self.fields['priority'].required = False


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description', 'icon']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Project name'}),
            'description': forms.Textarea(attrs={'rows': 3, 'placeholder': 'What is this project about?'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['description'].required = False
