from core.models import Exercises, Workouts, Workout_exercises, Workout_exercise_details, UserProfile
from core.models import Exercises, Workouts, Workout_exercises, Workout_exercise_details, UserProfile, Comment, Chatbot
from django.contrib import admin


# Register your models here.


@admin.register(Exercises)
class Exercise_Admin(admin.ModelAdmin):
    pass


@admin.register(Workouts)
class Workout_log_Admin(admin.ModelAdmin):
    pass


@admin.register(Workout_exercises)
class Workout_exercise_Admin(admin.ModelAdmin):
    pass


@admin.register(Workout_exercise_details)
class workout_exercise_detail_Admin(admin.ModelAdmin):
    pass


@admin.register(UserProfile)
class UserProfile_Admin(admin.ModelAdmin):
    pass


@admin.register(Comment)
class comment_Admin(admin.ModelAdmin):
    pass


@admin.register(Chatbot)
class Chatbot_Admin(admin.ModelAdmin):
    pass
