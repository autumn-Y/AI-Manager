from django.db import models
# Create your models here.


class Members(models.Model):
    id = models.CharField(help_text="User ID", max_length=20, primary_key=True)
    pswd = models.CharField(help_text="User Password", max_length=10, blank=False, null=False)
    name = models.CharField(max_length=10)
    email = models.CharField(max_length=20)
    location = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Exercise(models.Model):
    user_id = models.ForeignKey("Members", related_name="members", on_delete=models.DO_NOTHING, db_column="user_id")
    stretching = models.BooleanField(help_text="Like=True", default=False)
    home_training = models.BooleanField(help_text="Like=True", default=False)
    dance = models.BooleanField(help_text="Like=True", default=False)
    yoga = models.BooleanField(help_text="Like=True", default=False)
