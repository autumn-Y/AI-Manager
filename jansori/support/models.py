from django.db import models

# Create your models here.


class Members(models.Model):
    name = models.CharField(db_column='Name', max_length=20)  # Field name made lowercase.
    id = models.CharField(db_column='ID', primary_key=True, max_length=20)  # Field name made lowercase.
    pw = models.CharField(db_column='PW', max_length=20)  # Field name made lowercase.
    location = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'Members'

    objects = models.Manager()


class DailyRoutin(models.Model):
    id = models.OneToOneField(Members, models.DO_NOTHING, db_column='ID', primary_key=True)  # Field name made lowercase.
    recent_meal = models.DateTimeField(blank=True, null=True)
    recent_exercise = models.DateTimeField(blank=True, null=True)
    recent_clean = models.DateTimeField(blank=True, null=True)
    goal_meal = models.IntegerField(blank=True, null=True)
    goal_exercise = models.IntegerField(blank=True, null=True)
    goal_clean = models.IntegerField(blank=True, null=True)
    today_meal = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'daily_routin'
