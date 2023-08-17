from django.contrib import admin
from .models import CustomUser,Team,TeamMember,Task,TaskAssignment
# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Team)
admin.site.register(TeamMember)
admin.site.register(TaskAssignment)
admin.site.register(Task)