from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Admin(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    department=models.CharField(max_length=100,null=True)

    def __str__(self):
        return self.user.username

    
class Assignment(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    admin=models.ForeignKey(Admin,on_delete=models.CASCADE,related_name='assigned_tasks')
    task=models.TextField()
    file=models.FileField(upload_to="assignments/",null=True,blank=True)
    submittedAt=models.DateTimeField(auto_now_add=True)
    updatedAt=models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, default='pending', choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected')])

    def __str__(self):
        return self.task
    