from django.db import models
from django.utils import timezone

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


    


# Custom user model
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):

    ROLES = [
        ('manager', 'manager'),
        ('team leader', 'team leader'),
        ('team member','team member'),
    ]
     
    userid = models.AutoField(primary_key=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    firstname= models.CharField(max_length=100,unique=True)
    role=models.CharField(max_length=15, choices=ROLES, default= 'teammember')
    
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['role','firstname']
    
    objects = CustomUserManager()

# Team model
class Team(models.Model):
    teamid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    team_leader = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='led_teams')

    class Meta:
        unique_together = ['name', 'team_leader']
    def __str__(self):
        return self.name
# Team member model
class TeamMember(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)

    class Meta:
        unique_together = ['user', 'team']
    
    def __str__(self):
        return self.user.firstname

# Task model
class Task(models.Model):
   
    STATUSES = [
        ("CREATED",'Completed'),
        ("ASSIGNED", 'Assigned'),
        ("Inprogress", 'In progress'),
        ("UnderReview",'Under Review'),
        ("Done",'Done'),
    ]
    
    taskid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255,unique=True)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='tasks')
    status = models.CharField(max_length=12, choices=STATUSES, default="ASSIGNED")
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    @property
    def is_completed(self):
        return self.status == "Done"
    
    def save(self, *args, **kwargs):
        if self.status == "Done" and not self.completed_at:
            self.completed_at = timezone.now()
        elif self.status != "Done" :
            self.completed_at = None
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

# Task assignment model
class TaskAssignment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    
    class Meta:
    
      unique_together = ['task', 'user']

    def __str__(self):
        return self.task.name
