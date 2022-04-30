from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Workout(models.Model):
    owner = models.ForeignKey(User , on_delete=models.CASCADE )
    date = models.DateTimeField( auto_now_add=True, blank=False,null=False)
    description = models.CharField(max_length = 100, default ="",blank=True,null=True)

class Exercise(models.Model):
    owner = models.ForeignKey(User , on_delete=models.CASCADE )
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE)
    name = models.CharField(max_length = 50, default ="",blank=True,null=True)

class Set(models.Model):
    owner = models.ForeignKey(User , on_delete=models.CASCADE )
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    reps = models.IntegerField(blank=True, null=True, default=0)
    weight = models.IntegerField(blank=True, null=True, default=0)
