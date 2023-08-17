from django.db import models
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
    userid = models.AutoField(primary_key=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)

    ASSIGNED = 'Assigned'
    COMPLETED = 'Completed'
    
    STATUSES = [
        (ASSIGNED, 'Assigned'),
        (COMPLETED, 'Completed')
    ]
    
    
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    models.CharField(max_length=12, choices=ROLES, default= Team member)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    objects = CustomUserManager()

# Team model
class Team(models.Model):
    teamid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    team_leader = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='led_teams')

# Team member model
class TeamMember(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)

    class Meta:
        unique_together = ['user', 'team']

# Task model
class Task(models.Model):
    ASSIGNED = 'Assigned'
    COMPLETED = 'Completed'
    
    STATUSES = [
        (ASSIGNED, 'Assigned'),
        (COMPLETED, 'Completed')
    ]
    
    taskid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='tasks')
    status = models.CharField(max_length=12, choices=STATUSES, default=ASSIGNED)
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

# Task assignment model
class TaskAssignment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ['task', 'user']
