import datetime

from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db.models import CheckConstraint, F, Q, Max
from django.db.models.functions import Now
from django.urls import reverse
from django.utils import timezone

from Projekt.settings import STATIC_URL


def _upload_to(instance, filename):
    return STATIC_URL[1:] + '/images/' + str(instance.tournament.id) + "/" + filename


class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class MyUser(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=10, unique=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserManager()

    def __str__(self):
        return self.first_name + " " + self.last_name

class Tournament(models.Model):
    name = models.CharField(max_length=50)
    sport = models.CharField(max_length=50)
    start_date = models.DateTimeField()
    max_number_of_participants = models.IntegerField()
    registration_deadline = models.DateTimeField()
    country = models.CharField(max_length=50, blank=True, null=True)
    city = models.CharField(max_length=50)
    street = models.CharField(max_length=50)
    house_number = models.IntegerField()
    host_id = models.ForeignKey(MyUser, on_delete=models.PROTECT)

    class Meta:
        constraints = [
            CheckConstraint(
                check=Q(start_date__gt=F('registration_deadline')), name='check_start_date',
            ),
            CheckConstraint(
                check=Q(registration_deadline__gt=Now()), name='check_registration_deadline',
            ),
            CheckConstraint(check=Q(max_number_of_participants__gt=1), name='at least 2 participants'),
        ]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('tournaments', kwargs={'pk': self.pk})


class Sponsor(models.Model):
    logo = models.ImageField(upload_to=_upload_to)
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)


class Match(models.Model):
    winner_id = models.IntegerField(blank=True, null=True)
    player1_winner_pick = models.IntegerField(blank=True, null=True)
    player2_winner_pick = models.IntegerField(blank=True, null=True)
    tournament_phase = models.IntegerField()
    player1_id = models.ForeignKey(MyUser, on_delete=models.PROTECT, related_name='player 1+', blank=True, null=True)
    player2_id = models.ForeignKey(MyUser, on_delete=models.PROTECT, related_name='player 2+', blank=True, null=True)
    tournament_id = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    date = models.DateTimeField()
    number = models.IntegerField()

    def __str__(self):
        if self.winner_id == -1:
            return "Phase: " + self.getPhaseName() + "\nMatch wasn't played because there wasn't enough participants registered."
        return "Phase: " + self.getPhaseName() +\
                   "\nLatest possible match date: " + str(self.date.strftime("%Y-%m-%d %H:%M:%S")) + "\nWinner: " + self.getWinnerName()

    def getPhaseName(self):
        if self.tournament_phase == 1:
            return "Final"
        elif self.tournament_phase == 2:
            return "Semi-final"
        elif self.tournament_phase == 3:
            return "Quarter-final"
        else:
            return "Round of " + str(2 ** self.tournament_phase)

    def getWinnerName(self):
        if self.winner_id is None:
            return "TBD"
        elif self.player1_id.id is not None and self.winner_id == self.player1_id.id:
            toReturn = self.player1_id.first_name + " " + self.player1_id.last_name
            if self.player2_id is None:
                toReturn += " (no opponent)"
        else:
            toReturn = self.player2_id.first_name + " " + self.player2_id.last_name
            if self.player1_id is None:
                toReturn += " (no opponent)"
        return toReturn


class Participation(models.Model):
    user_id = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    tournament_id = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    ranking = models.IntegerField()
    license_number = models.CharField(max_length=50)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['tournament_id', 'ranking'], name='unique ranking'),
            models.UniqueConstraint(fields=['tournament_id', 'license_number'], name='unique license number'),
            models.UniqueConstraint(fields=['tournament_id', 'user_id'], name='one registration per user'),
            CheckConstraint(check=Q(ranking__gt=0), name='positive ranking'),
        ]

    def __str__(self):
        return "Player: " + self.user_id.first_name + " " + self.user_id.last_name + " Ranking: " + str(self.ranking)
