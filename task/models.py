from django.db import models
from django.utils.timezone import now
from user.models import User
from django.core.exceptions import ValidationError

class Task(models.Model):

    status_choices = (('P',"Pending"),('D',"Done"))
    priority_choices = (('U','Urgnet'),('I','Important'),('IU','Important and urgent'),('C','Casual'))

    name = models.CharField(max_length=80)
    priority = models.CharField(max_length=2,choices= priority_choices,default='C')
    description = models.TextField(blank=True)
    date_created = models.DateTimeField(auto_now_add=True , editable=False)
    expiration_date = models.DateTimeField(null=True , blank= True)
    status = models.CharField(max_length=1,choices=status_choices , default='P')
    user = models.ForeignKey(User , on_delete= models.CASCADE , related_name='tasks')

    class Meta:
        ordering = ['expiration_date']  # orders tasks by expiration date
    
    def clean(self):
        # Check if expiration_date exists (not None)
        if self.expiration_date and self.date_created:
            if self.expiration_date <= self.date_created:
                raise ValidationError({
                    'expiration_date': 'Expiration date must be after the creation date.'
                })
            
    def save(self, *args, **kwargs):
        self.full_clean()  # This calls clean() before saving
        super().save(*args, **kwargs)
    

