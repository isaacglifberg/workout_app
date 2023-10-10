from django.core.mail import send_mail
from django.conf import settings
from django_q.tasks import async_task, schedule, Schedule
from datetime import timedelta
from django.utils import timezone


def send_email(recipient_list, username):
    subject = f'New message from {username}'
    message = f'{username} has completed a workout. Go check it out'
    from_email = settings.EMAIL_HOST_USER
    send_mail(subject, message, from_email, recipient_list)


def email_task(recipient_list, username):
    async_task(send_email, recipient_list, username)


def scheduled_mail_welcome(recipient_list, username):
    subject = 'Welcome mail'
    message = f' Welcome {username} to our workout app! Here you can log your workout and much more.'
    from_email = settings.EMAIL_HOST_USER
    schedule(
        "django.core.mail.send_mail",
        subject,
        message,
        from_email,
        recipient_list,
        schedule_type=Schedule.ONCE,
        next_run=timezone.now() + timedelta(minutes=30))
