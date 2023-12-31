# Generated by Django 4.2.4 on 2023-08-18 18:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TaskTracker', '0004_customuser_firstname'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='role',
            field=models.CharField(choices=[('manager', 'manager'), ('teamLead', 'team leader'), ('teammember', 'team member')], default='teammember', max_length=15),
        ),
        migrations.AlterField(
            model_name='task',
            name='status',
            field=models.CharField(choices=[('CREATED', 'Completed'), ('ASSIGNED', 'Assigned'), ('Inprogress', 'In progress'), ('UnderReview', 'Under Review'), ('Done', 'Done')], default='Assigned', max_length=12),
        ),
        migrations.AlterUniqueTogether(
            name='team',
            unique_together={('name', 'team_leader')},
        ),
    ]
