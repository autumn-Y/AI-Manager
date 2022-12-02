import datetime

from django.db import models


class User(models.Model):
    name = models.CharField(max_length=20)
    user_id = models.CharField(max_length=30, primary_key=True)
    pw = models.CharField(max_length=30)
    location = models.CharField(max_length=30, default='서울시 성동구')

    objects = models.Manager()

    def __str__(self):
        return self.user_id

    class Meta:
        db_table = 'user'


class Goal(models.Model):
    goal_id = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, db_column='goal_id')
    meal = models.IntegerField()
    exercise = models.IntegerField()
    clean = models.IntegerField()

    class Meta:
        db_table = 'goal'

    objects = models.Manager()


class Recent(models.Model):
    recent_id = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, db_column='recent_id')
    recent_meal = models.DateTimeField(blank=True, default=datetime.datetime.now())
    meal_count = models.IntegerField(blank=True, default=0)
    recent_exercise = models.DateTimeField(blank=True, default=datetime.datetime.now())
    recent_clean = models.DateTimeField(blank=True, default=datetime.datetime.now())

    class Meta:
        db_table = 'recent'

    objects = models.Manager()


class HomeConnect(models.Model):
    home_id = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, db_column='home_id')
    air_conditioner_name = models.CharField(max_length=30)
    air_purifier_name = models.CharField(max_length=30)
    tv_name = models.CharField(max_length=30)
    robot_clean_name = models.CharField(max_length=30)

    class Meta:
        db_table = 'homeconnect'

    objects = models.Manager()


class TurnOn(models.Model):
    turnon_id = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, db_column='home_id')
    air_conditioner = models.BooleanField(default=0)
    air_purifier = models.BooleanField(default=0)
    tv = models.BooleanField(default=0)
    robot_clean = models.BooleanField(default=0)

    class Meta:
        db_table = 'turnon'

    objects = models.Manager()


