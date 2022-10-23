from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    division = models.CharField(max_length=100, blank=True, null=True)
    avatar = models.CharField(max_length=500, blank=True, null=True)
    behaviour   = models.IntegerField(default=0)
    compliance  = models.IntegerField(default=0)
    progress    = models.IntegerField(default=0)
    score       = models.IntegerField(default=0)

    def __str__(self) -> str:
        return self.user.username

    # get the total number of users (employees)
    def getAllEmployees(self, request):
        return sum(User.objects.all())
        

@receiver(post_save, sender=User)
def create_or_update_user_profile(self, sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()


class Task(models.Model):
    user        = models.ForeignKey(User, on_delete=models.CASCADE)
    subject     = models.TextField(max_length=1000, blank=True, null=True)
    start_date  = models.CharField(max_length= 100, blank=True, null=True)
    end_date    = models.CharField(max_length=100, blank=True, null=True)
    start_day   = models.CharField(max_length=100, blank=True, null=True)  
    end_day     = models.CharField(max_length=100, blank=True, null=True)
    no_of_users = models.IntegerField(default=0)
    employees   = models.ManyToManyField(User, related_name="employees")
    TASK_STATUS = [
      ("غير منجزة", "غير منجزة"),
      ("بأنتظار الموافقة", "بأنتظار الموافقة"),
      ("منجزة", "منجزة")
    ]
    status      = models.CharField(max_length=100, choices=TASK_STATUS, default="غير منجزة")
    received    = models.BooleanField(default=False)
    created_at  = models.DateTimeField(auto_now_add=True)   
    def __str__(self):
      return self.subject

    # get the total tasks (tasks created by staff members)
    def getStaffTasks(self, request):
        return sum(not task.user.is_superuser for task in Task.objects.all())
    
    # get the total tasks (tasks acheived by users)
    def getAcheivedTasks(self, request):
        return sum(task.status == "منجزة" for task in Task.objects.all())
    
    # get the total tasks (tasks not acheived by users)
    def getNotAcheivedTasks(self, request):
        return sum(task.status == "غير منجزة" for task in Task.objects.all())