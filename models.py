from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    weight = models.IntegerField(null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    number_of_workouts = models.IntegerField(null=True, blank=True)


class Exercises(models.Model):
    BODY_PARTS = (
        ('Forearms', 'Forearms'),
        ('Triceps', 'Triceps'),
        ('Biceps', 'Biceps'),
        ('Neck', 'Neck'),
        ('Shoulders', 'Shoulders'),
        ('Chest', 'Chest'),
        ('Back', 'Back'),
        ('Core', 'Core'),
        ('Upper Legs', 'Upper Legs'),
        ('Glutes', 'Glutes'),
        ('Calves', 'Calves'),
        ('Full Body', 'Full Body'),
        ('Other', 'Other'),
    )
    EQUIPMENT = (
        ('Barbell', 'Barbell'),
        ('Dumbbell', 'Dumbbell'),
        ('Machine', 'Machine'),
        ('Bodyweight', 'Bodyweight'),
        ('Other', 'Other'),
    )
    name = models.CharField(max_length=64)
    description = models.TextField(max_length=512, blank=True, null=True)
    body_part = models.CharField(max_length=16, choices=BODY_PARTS)
    equipment = models.CharField(max_length=16, choices=EQUIPMENT)

    def __str__(self):
        return self.name


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    workout = models.ForeignKey(
        'Workouts', on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)


class Workouts(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='workouts')
    time_start = models.DateTimeField(blank=True, null=True)
    time_end = models.DateTimeField(blank=True, null=True)
    duration = models.DurationField(blank=True, null=True)


class Workout_exercises(models.Model):
    workout = models.ForeignKey(
        Workouts, related_name="workout_exercises", on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercises, on_delete=models.CASCADE)


class Workout_exercise_details(models.Model):
    workout_exercise = models.ForeignKey(Workout_exercises, related_name="workout_exercise_details",
                                         on_delete=models.CASCADE)
    sets = models.PositiveIntegerField()
    reps = models.PositiveIntegerField()
    weight = models.PositiveIntegerField()


class Chatbot(models.Model):
    query = models.CharField(max_length=50)
    responses = models.CharField(max_length=50)
    tag = models.CharField(max_length=50)
