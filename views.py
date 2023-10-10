from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from core.models import Exercises, Workouts, Workout_exercises, Workout_exercise_details, Comment, UserProfile
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.utils import timezone
from core.tasks import scheduled_mail_welcome, email_task
from django.http import JsonResponse

# Create your views here.


def home(request):
    return render(request, "home.html", {})


def signup(request):
    user_emails = User.objects.values_list('email')
    list_emails = [email for tuples in user_emails for email in tuples]
    if request.method == 'POST':
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        password = request.POST['password']
        weight = request.POST.get('weight')
        if weight == '':
            weight = None
        birth_date = request.POST.get('birth_date')
        if birth_date == '':
            birth_date = None

        errors = {}
        if not username:
            errors['username'] = 'Username is required'
        emails = User.objects.values_list('email')
        for user_email in emails:
            for x in user_email:
                if x == email:
                    errors['email'] = 'Email already exists'
        if '@' not in email:
            errors['email'] = 'Email most have @ '
        if not fname:
            errors['fname'] = 'First name is required'
        elif fname.isalpha() == False:
            errors['fname'] = 'First name can only contain letters'
        if not lname:
            errors['lname'] = 'Last name is required'
        elif lname.isalpha() == False:
            errors['lname'] = 'Last name can only contain letters'
        if not errors:
            try:
                some_user = User.objects.create_user(username, email, password)
                scheduled_mail_welcome(list_emails, username)
                some_user.first_name = fname
                some_user.last_name = lname
                some_user.save()
                new_profile = UserProfile.objects.create(
                    user=some_user, weight=weight, birth_date=birth_date)
                return redirect('signin')
            except IntegrityError:
                errors['username'] = 'Username already exists'
    else:
        errors = {}
    return render(request, 'signup.html', {'errors': errors})


def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('profile')
        else:
            error_message = "Invalid username or password"
    else:
        error_message = None

    return render(request, "signin.html", {'error_message': error_message})


def signout(request):
    logout(request)
    return redirect('signin')


@login_required
def start_workout(request):
    error_message = ''
    if request.method == 'POST':
        exercise_ids = request.POST.getlist('exercises')
        workout = Workouts.objects.create(
            user=request.user, time_start=timezone.now())
        if not exercise_ids:
            error_message = 'Please select a exercise'
        else:
            for exercise_id in exercise_ids:
                exercise = Exercises.objects.get(pk=exercise_id)
                Workout_exercises.objects.create(
                    workout=workout, exercise=exercise)
            return redirect('save_workout', workout_id=workout.id)

    exercises = Exercises.objects.all()
    return render(request, 'start_workout.html', {'exercises': exercises, 'error_message': error_message})


def add_exercise(request):
    errors = ''
    if request.method == 'POST':
        body_part = request.POST.get('body_part')
        equipment = request.POST.get('equipment')
        description = request.POST.get('description')
        name = request.POST.get('name')
        if not body_part:
            errors = 'Please choose a body part'
        if not equipment:
            errors = 'Please choose a equipment'
        if not errors:
            Exercises.objects.create(
                body_part=body_part, equipment=equipment,  description=description, name=name)
            return redirect('start_workout')
    exercises = Exercises.objects.all()
    return render(request, 'start_workout.html', {'errors': errors, 'exercises': exercises})


@login_required
def save_workout(request, workout_id):
    error_message = ''
    username = request.user.username
    user_emails = User.objects.values_list('email')
    list_emails = [email for tuples in user_emails for email in tuples]
    workout = Workouts.objects.get(pk=workout_id)
    workout_exercises = workout.workout_exercises.all()
    if request.method == 'POST':
        workout.time_end = timezone.now()
        workout.duration = workout.time_end - workout.time_start
        workout.save()
        for workout_exercise in workout_exercises:
            sets = request.POST.get('sets_' + str(workout_exercise.id))
            reps = request.POST.get('reps_' + str(workout_exercise.id))
            weight = request.POST.get('weight_' + str(workout_exercise.id))
            if sets == "0" or reps == '0' or weight == '0':
                error_message = 'Values must be greater than zero'
            elif not sets.isnumeric() or not reps.isnumeric() or not weight.isnumeric():
                error_message = 'Values can not be empty'
            else:
                Workout_exercise_details.objects.create(
                    workout_exercise=workout_exercise, sets=sets, reps=reps, weight=weight)
        email_task(list_emails, username)
        return redirect('feed')

    return render(request, 'save_workout.html', {'workout': workout, 'workout_exercises': workout_exercises, 'error_message': error_message})


@login_required
def display_profile(request):
    workouts = Workouts.objects.filter(user=request.user).order_by('-time_end')
    workout_data = []
    for workout in workouts:
        exercise_data = []
        workout_exercises = Workout_exercises.objects.filter(workout=workout)
        for workout_exercise in workout_exercises:
            exercise = workout_exercise.exercise
            exercise_details = Workout_exercise_details.objects.filter(
                workout_exercise=workout_exercise)
            exercise_data.append(
                {'exercise': exercise, 'details': exercise_details})
        workout_data.append({'workout': workout, 'exercises': exercise_data})
    user_profile = UserProfile.objects.get(user=request.user)
    workouts = Workouts.objects.all()

    context = {
        'workout_data': workout_data,
        'user_profile': user_profile,
        'workouts': workouts
    }
    return render(request, 'display_profile.html', context,)


@login_required
def display_feed(request):
    workouts = Workouts.objects.all().order_by('-time_end')
    workout_data = []
    for workout in workouts:
        exercise_data = []
        workout_exercises = Workout_exercises.objects.filter(workout=workout)
        for workout_exercise in workout_exercises:
            exercise = workout_exercise.exercise
            exercise_details = Workout_exercise_details.objects.filter(
                workout_exercise=workout_exercise)
            exercise_data.append(
                {'exercise': exercise, 'details': exercise_details})
        comments = workout.comments.all()
        workout_data.append({
            'workout': workout,
            'exercises': exercise_data,
            'comments': comments
        })

    context = {
        'workout_data': workout_data,
    }
    return render(request, 'feed.html', context)


@login_required
def add_comment(request, workout_id):
    if request.method == 'POST':
        workout = Workouts.objects.get(id=workout_id)
        comment_text = request.POST['comment']
        comment = Comment.objects.create(
            workout=workout, user=request.user, content=comment_text)
        comment.save()
    return redirect('feed')


@login_required
def edit_profile(request):
    user = request.user
    user_instance = User.objects.get(username=user.username)
    count_workouts = user_instance.workouts.count()

    user_profile = request.user.userprofile

    if request.method == 'POST':
        weight = request.POST.get('weight')
        if weight == '':
            weight = None
        birth_date = request.POST.get('birth_date')
        if birth_date == '':
            birth_date = None

        user_profile.weight = weight
        user_profile.birth_date = birth_date
        user_profile.number_of_workouts = count_workouts
        user_profile.save()

        return redirect('profile')

    context = {
        'user_profile': user_profile,
    }

    return render(request, 'edit_profile.html', context)


@login_required
def delete_workout(request, id):
    user = request.user
    Workouts.objects.get(id=id, user=user).delete()
    return redirect('profile')


@login_required
def chatbot_view(request):
    if request.method == 'POST':
        message = request.POST['message']
        if message == " ":
            message == None

    return render(request, 'chatbot.html')
