from django import forms
from task.models import Task

class CreateTask(forms.ModelForm):
    
    class Meta:
        model = Task
        fields = '__all__'
        exclude = ['date_created','status','user',]
        widgets = {
            'expiration_date': forms.DateInput(
                attrs={'type': 'date',}
            ),
            'description':forms.TextInput()
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['description'].required = False
        self.fields['expiration_date'].required = False
        self.fields['priority'].required = False