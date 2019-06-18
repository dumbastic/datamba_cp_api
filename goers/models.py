from django.db import models

# Create your models here.
class Training(models.Model):
    algorithm = models.CharField(max_length=30)
    test_size = models.FloatField()
    train_accuracy = models.FloatField()
    test_accuracy = models.FloatField()

class Recommendation(models.Model):
    prediction = models.IntegerField()
    description = models.CharField(max_length=10)