import datetime

from django.db.models import CheckConstraint, Q, F
from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.admin import widgets
from django.forms import widgets
from .models import *
from django.utils import timezone


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=50, help_text='Required.')
    last_name = forms.CharField(max_length=50, help_text='Required.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = MyUser
        fields = ('first_name', 'last_name', 'email', 'password1', 'password2')


class TournamentForm(ModelForm):
    class Meta:
        model = Tournament
        fields = ['name', 'sport', 'start_date', 'registration_deadline', 'city', 'street', 'house_number', 'max_number_of_participants']
        help_texts = {
            'start_date': 'Date format: YYYY-MM-DD HH:MM:SS',
            'registration_deadline': 'Date format: YYYY-MM-DD HH:MM:SS'
        }

    def clean(self):
        cleaned_data = super().clean()

        try:
            deadline = cleaned_data["registration_deadline"]
            start_date = cleaned_data["start_date"]
        except KeyError:
            pass
        else:
            if start_date < deadline:
                msg = u"Start date must be later than registration deadline"
                self._errors["start_date"] = self.error_class([msg])
            if deadline <= timezone.now():
                msg = u"You can't add tournament from the past"
                self._errors["registration_deadline"] = self.error_class([msg])
        return cleaned_data


class SponsorForm(ModelForm):
    logo = forms.ImageField()

    class Meta:
        model = Sponsor
        fields = ('logo',)


class JoinForm(ModelForm):
    class Meta:
        model = Participation
        fields = ('ranking', 'license_number')

    def clean(self):
        cleaned_data = super().clean()

        try:
            ranking = cleaned_data["ranking"]
        except KeyError:
            pass
        else:
            if ranking <= 0:
                msg = u"Ranking must be positive integer"
                self._errors["ranking"] = self.error_class([msg])
        return cleaned_data


class PostMatchWinnerForm(ModelForm):
    player_winner_pick = forms.ModelChoiceField(queryset=MyUser.objects.all())
    player_winner_pick.label = "Winner pick"

    class Meta:
        model = Match
        fields = ('player_winner_pick',)
