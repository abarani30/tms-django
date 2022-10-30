from email.policy import default
from random import choices
from typing import List
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


# Profile table
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    division = models.CharField(max_length=100, blank=True, null=True)
    avatar = models.CharField(max_length=500, blank=True, null=True)
    ACCOUNT_TYPE = [
      ("ادمن", "ادمن"),
      ("محرر", "محرر"),
      ("مستخدم", "مستخدم")
    ]
    account     = models.CharField(max_length=100, choices=ACCOUNT_TYPE, default="مستخدم")
    behaviour   = models.IntegerField(default=0)
    compliance  = models.IntegerField(default=0)
    progress    = models.IntegerField(default=0)
    score       = models.IntegerField(default=0)

    def __str__(self) -> str:
        return self.user.username

    # get the total number of users (employees)
    def getAllEmployees(self):  # sourcery skip: simplify-generator
        return User.objects.all().count()


# link the current profile with the existing user
@receiver(post_save, sender=User)
def create_or_update_user_profile(instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()


# Task table
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
    TASK_RATE = [
      (20, 20),
      (40, 40),
      (60, 60),
      (80, 80),
      (100, 100),
    ]
    rate        = models.CharField(max_length=100, choices=TASK_RATE, default=20)

    received    = models.BooleanField(default=False)
    active      = models.BooleanField(default=True)
    created_at  = models.DateTimeField(auto_now_add=True)   
    
    # display the tasks subject in the admin panel
    def __str__(self):
      return self.subject

    # count the total tasks (tasks created by staff members)
    def countStaffTasks(self):
        return sum(not task.user.is_superuser for task in Task.objects.all())
    
    # count the total tasks (tasks acheived by users)
    def countAcheivedTasks(self):
        return sum(task.status == "منجزة" and not task.user.is_superuser for task in Task.objects.all())
    
    # count the total tasks (tasks not acheived by users)
    def countNotAcheivedTasks(self):
        return sum(task.status == "غير منجزة" and not task.user.is_superuser for task in Task.objects.all())

    # get the last three tasks (tasks created by staff members)
    def getLastThree(self):
        return Task.objects.prefetch_related("employees").order_by("-created_at")[:3]

    # count the total tasks for the systems division
    def countSystemsTasks(self):
        week: List[str] = ["الاحد", "الاثنين", "الثلاثاء", "الاربعاء", "الخميس"]
        return [sum(task.start_day == day and task.user.profile.division == "الانظمة" and not task.user.is_superuser for task in Task.objects.all()) for day in week]
    
    # count the total tasks for the systems division
    def countMaintenanceTasks(self):
        week: List[str] = ["الاحد", "الاثنين", "الثلاثاء", "الاربعاء", "الخميس"]
        return [sum(task.start_day == day and task.user.profile.division == "الفنية" and not task.user.is_superuser for task in Task.objects.all()) for day in week]

# Notification table
class Notification(models.Model):
    user        = models.ForeignKey(User, on_delete=models.CASCADE)
    message     = models.TextField(max_length=1000, blank=True, null=True)
    emps        = models.ManyToManyField(User, related_name="emps")
    created_at  = models.DateTimeField(auto_now_add=True)
    received    = models.BooleanField(default=False)

    def __str__(self):
        return self.message 

    # count the total unreadable notifications for the current user 
    def countUnreadableNotifications(self, request):
        return sum(
            not notification.received and request.user in notification.emps.all()
            for notification in Notification.objects.all())

    # count the total notifications (readable and unreadable) for the current user
    def countTotalNotifications(self, request):
        return sum(request.user in notification.emps.all()
            for notification in Notification.objects.all()) 

    # get the total notifications for the current user 
    def getUserNotifications(self, request):
        return [
            notification for notification in Notification.objects.all()
            .order_by("-created_at")
            if request.user in notification.emps.all()
        ]