from django.urls import path, include
from django.contrib.auth import views as auth_views

from . import views

app_name = 'tournaments'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.TournamentView.as_view(), name='tournament'),
    path('matches/<int:pk>/', views.MatchView.as_view(), name='match'),
    path('redirect/', views.redirect_view, name='redirect'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('registration/finalized', views.signup, name='registration_done'),
    path('activate/<uidb64>/<token>', views.registration_finalized_view, name='registration_confirm'),
    path('add/', views.TournamentCreate.as_view(), name='addtournament'),
    path('<int:pk>/edit/', views.TournamentUpdate.as_view(), name='edittournament'),
    path('sponsor/add/', views.logo_upload, name='addsponsor'),
    path('<int:pk>/register/', views.JoinTournament.as_view(), name='takepart'),
    path('<int:pk>/mytournaments', views.MyMatchesView.as_view(), name='mymatches'),
]
