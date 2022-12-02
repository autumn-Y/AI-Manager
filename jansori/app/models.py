from django.db import models

# user information
class User(models.Model):
    name = models.CharField(max_length=30)
    user_id = models.CharField(max_length=30)
    pw = models.CharField(max_length=30)
    location = models.CharField(max_length=30, default='서울시 성동구')

    objects = models.Manager()

    def __str__(self):
        return self.user_id

    class Meta:
        db_table = 'user'


class Goal(models.Model):
    goal_id = models.ForeignKey(User, on_delete=models.CASCADE, db_column='goal_id')
    meal = models.IntegerField()
    exercise = models.IntegerField()
    clean = models.IntegerField()

    class Meta:
        db_table = 'goal'

    objects = models.Manager()


class Recent(models.Model):
    recent_id = models.ForeignKey(User, on_delete=models.CASCADE, db_column='goal_id')
    recent_meal = models.DateTimeField()
    meal_count = models.IntegerField()
    recent_exercise = models.DateTimeField()
    recent_clean = models.DateTimeField()

    class Meta:
        db_table = 'recent'

    objects = models.Manager()
