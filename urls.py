from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('home', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('signout/', views.signout, name='signout'),
    path('start_workout/', views.start_workout, name='start_workout'),
    path('save_workout/<int:workout_id>/',
         views.save_workout, name='save_workout'),
    path('profiles/',
         views.display_profile, name='profile'),
    path('feed/',
         views.display_feed, name='feed'),
    path('add_exercise/', views.add_exercise, name='add_exercise'),
    path('add_comment/<int:workout_id>/',
         views.add_comment, name='add_comment'),
    path('delete_workout/<int:id>/', views.delete_workout, name='delete_workout'),

    path('reset_password/', auth_views.PasswordResetView.as_view(
         template_name='password_reset.html'
         ), name='password_reset'),
    path('reset_password/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='password_reset_done.html'
    ), name='password_reset_done'),
    path('reset_password/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='password_reset_confirm.html'
    ), name='password_reset_confirm'),
    path('reset_password/complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='password_reset_complete.html'
    ), name='password_reset_complete'),

    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('chatbot/', views.chatbot_view, name='chatbot'),


]
