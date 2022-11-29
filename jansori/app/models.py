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
    recent_meal = models.DateTimeField(default=datetime.datetime.now())
    meal_count = models.IntegerField(default=0)
    recent_exercise = models.DateTimeField(default=datetime.datetime.now())
    recent_clean = models.DateTimeField(default=datetime.datetime.now())

    class Meta:
        db_table = 'recent'

    objects = models.Manager()
