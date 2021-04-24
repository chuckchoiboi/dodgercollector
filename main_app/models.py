from django.db import models

# Import the reverse function
from django.urls import reverse

from datetime import date

from django.contrib.auth.models import User


WORKOUTS = (
    ('W', 'Weight'),
    ('C', 'Cardio'),
    ('B', 'Batting'),
    ('P', 'Position Training')
)

# Create your models here.


class Equipment(models.Model):
    name = models.CharField(max_length=50)
    brand = models.CharField(max_length=20)

    def __str__(self):
        return f'{self.name} {self.brand}'

    def get_absolute_url(self):
        return reverse('equipment_detail', kwargs={'equipment_id': self.id})

        class Meta:
            ordering = ['-date']


class Dodger(models.Model):
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    description = models.TextField(max_length=250)
    salary = models.CharField(max_length=100)
    equipments = models.ManyToManyField(Equipment)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('detail', kwargs={'dodger_id': self.id})

    def trained_for_today(self):
        return self.training_set.filter(date=date.today()).count() >= len(WORKOUTS)


class Training(models.Model):
    date = models.DateField('training date')
    workout = models.CharField(
        max_length=1, choices=WORKOUTS, default=WORKOUTS[0][0])
    dodger = models.ForeignKey(Dodger, on_delete=models.CASCADE)

    def __str__(self):
        # Nice method for obtaining the friendly value of a Field.choice
        return f"{self.get_workout_display()} on {self.date}"

    class Meta:
        ordering = ['-date']


class Photo(models.Model):
    url = models.CharField(max_length=200)
    dodger = models.ForeignKey(Dodger, on_delete=models.CASCADE)

    def __str__(self):
        return f"Photo for dodger_id: {self.dodger_id} @{self.url}"
