import datetime

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site
from django.core.checks import messages
from django.db.models import Count, Max
from django.forms import modelformset_factory
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views import generic
from django.core.mail import EmailMessage
from django.views.generic import FormView, CreateView, UpdateView
from django.views.generic.edit import FormMixin

from Projekt.settings import BASE_DIR
from .models import *
from .forms import TournamentForm, SponsorForm, SignUpForm, JoinForm, PostMatchWinnerForm
from math import log2, ceil, floor


def bracketLayer(bracket):
    out = []
    length = len(bracket) * 2 + 1
    for number in bracket:
        out.append(number)
        out.append(length - number)
    return out


def seed(rounds):
    seeding_list = [1, 2]
    for i in range(rounds):
        seeding_list = bracketLayer(seeding_list)
    for i in range(len(seeding_list)):
        seeding_list[i] -= 1
    return seeding_list


def generateBracket(tournament):
    number_of_stages = ceil(log2(tournament.max_number_of_participants))
    number_of_matches = 2 ** number_of_stages - 1
    seeding = seed(number_of_stages - 1)
    participation_list = list(Participation.objects.filter(tournament_id=tournament).order_by('ranking'))
    index = 0
    matches = [None] * (number_of_matches + 1)
    for i in range(number_of_matches, 2 ** floor(log2(number_of_matches)) - 1, -1):
        matches[i] = Match(number=i, tournament_phase=number_of_stages, tournament_id=tournament,
                           date=tournament.start_date + timezone.timedelta(hours=3 * (number_of_matches - i + 1)))
        if len(participation_list) > seeding[index]:
            matches[i].player1_id = participation_list[seeding[index]].user_id
        else:
            matches[i].player1_id = None
        index += 1
        if len(participation_list) > seeding[index]:
            matches[i].player2_id = participation_list[seeding[index]].user_id
        else:
            matches[i].player2_id = None
        index += 1

        if matches[i].player1_id is None and matches[i].player2_id is None:
            matches[i].winner_id = -1
        elif matches[i].player1_id is None and matches[i].player2_id is not None:
            matches[i].winner_id = matches[i].player2_id.id
        elif matches[i].player1_id is not None and matches[i].player2_id is None:
            matches[i].winner_id = matches[i].player1_id.id
        else:
            matches[i].winner_id = None

    for i in range(number_of_matches // 2, 0, -1):
        matches[i] = Match(number=i, tournament_phase=ceil(log2(i + 1)), tournament_id=tournament,
                           date=tournament.start_date + timezone.timedelta(hours=3 * (number_of_matches - i + 1)))
        childMatch1 = matches[i * 2 + 1]
        childMatch2 = matches[i * 2]
        willPlayer1Arrive = True
        willPlayer2Arrive = True
        if childMatch1.winner_id == -1:
            willPlayer1Arrive = False
        if childMatch2.winner_id == -1:
            willPlayer2Arrive = False
        matches[i].player1_id = MyUser.objects.filter(id=childMatch1.winner_id).first()
        matches[i].player2_id = MyUser.objects.filter(id=childMatch2.winner_id).first()

        if matches[i].player1_id is None and matches[i].player2_id is None: # NONE == TBD; -1 == NOT PLAYED
            if (not willPlayer1Arrive) and (not willPlayer2Arrive):
                matches[i].winner_id = -1
            else:
                matches[i].winner_id = None
        elif not willPlayer1Arrive:
            matches[i].winner_id = matches[i].player2_id.id
        elif not willPlayer2Arrive:
            matches[i].winner_id = matches[i].player1_id.id

    for match in matches:
        if match is not None:
            match.save()


token_generator = PasswordResetTokenGenerator()


class IndexView(generic.ListView):
    template_name = 'tournaments/index.html'
    context_object_name = 'latest_tournaments_list'
    paginate_by = 10

    def get_queryset(self):
        if 'query' in self.request.GET.keys():
            return Tournament.objects.annotate(num_participants=Count('participation'))\
                .filter(registration_deadline__gte=datetime.datetime.now())\
                .filter(name__contains=self.request.GET['query'])\
                .order_by('registration_deadline')
        else:
            return Tournament.objects.annotate(num_participants=Count('participation')) \
                .filter(registration_deadline__gte=datetime.datetime.now()) \
                .order_by('registration_deadline')


class TournamentView(FormMixin, generic.DetailView):
    model = Tournament
    form_class = PostMatchWinnerForm
    template_name = 'tournaments/tournament.html'
    success_url = '/tournaments/'


    def post(self, request, *args, **kwargs):
        self.success_url += str(self.request.session['tournament'])
        form = self.get_form()

        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        chosen_player = form.cleaned_data['player_winner_pick']
        tournament_matches = Match.objects.filter(tournament_id=self.get_object())
        match = tournament_matches.filter(Q(player1_id=self.request.user) | Q(player2_id=self.request.user))\
            .filter(winner_id=None)\
            .filter(~Q(player1_id=None))\
            .filter(~Q(player2_id=None)).first()
        if match.player1_id == self.request.user:
            match.player1_winner_pick = chosen_player.id
        else:
            match.player2_winner_pick = chosen_player.id
        if match.player1_winner_pick is not None and match.player2_winner_pick is not None:
            if match.player1_winner_pick == match.player2_winner_pick:
                match.winner_id = match.player2_winner_pick
                match.save()
                self.update_bracket(tournament_matches, match.number)
            else:
                match.player1_winner_pick = None
                match.player2_winner_pick = None
                match.save()
        else:
            match.save()
        return super().form_valid(form)

    def update_bracket(self, matches, match_number):
        next_match_number = match_number // 2
        matchToUpdate = matches.filter(number=next_match_number).first()
        previousMatch = matches.filter(number=match_number).first()
        winner = MyUser.objects.filter(id=previousMatch.winner_id).first()
        if matchToUpdate is None:
            return
        if match_number == next_match_number * 2:
            matchToUpdate.player2_id = winner
        else:
            matchToUpdate.player1_id = winner
        matchToUpdate.save()


    def get_context_data(self, **kwargs):
        self.request.session['tournament'] = self.get_object().id
        context = super(TournamentView, self).get_context_data(**kwargs)
        context['numOfParticipants'] = Tournament.objects.filter(id=self.get_object().id).annotate(num_participants=Count('participation'))
        if self.get_object().registration_deadline < timezone.now():
            context['from_past'] = True
        else:
            context['from_past'] = False
        paths = Sponsor.objects.filter(tournament=self.get_object()).values_list('logo')
        context['imagePaths'] = []
        for i in paths:
            context['imagePaths'].append(BASE_DIR + '/' + i[0])
        context['matches'] = Match.objects.filter(tournament_id=self.get_object()).order_by('-number')
        if self.get_object().registration_deadline < timezone.now() and len(context['matches']) == 0:
            generateBracket(self.get_object())
            context['matches'] = Match.objects.filter(tournament_id=self.get_object()).order_by('-number')
        if self.request.user.is_authenticated and self.get_object().start_date < timezone.now():
            context['upcomingMatch'] = context['matches'].filter(Q(player1_id=self.request.user) | Q(player2_id=self.request.user)).filter(winner_id=None)\
                .filter(~Q(player1_id=None))\
                .filter(~Q(player2_id=None))\
                .order_by("-date").first()
            if context['upcomingMatch'] is not None:
                if self.request.user.id == context['upcomingMatch'].player1_id.id:
                    context['userPick'] = MyUser.objects.filter(id=context['upcomingMatch'].player1_winner_pick).first()
                if self.request.user.id == context['upcomingMatch'].player2_id.id:
                    context['userPick'] = MyUser.objects.filter(id=context['upcomingMatch'].player2_winner_pick).first()
                if self.request.method == "GET":
                    context['form'] = PostMatchWinnerForm()
                    context['form'].fields['player_winner_pick'].queryset = MyUser.objects.filter(
                                    Q(id=context['upcomingMatch'].player1_id.id) | Q(id=context['upcomingMatch'].player2_id.id))
                    context['form'].fields['player_winner_pick'].initial = context['userPick']

        return context


class MatchView(generic.DetailView):
    model = Match
    template_name = 'tournaments/matchList.html'


class MyMatchesView(generic.ListView):
    template_name = 'tournaments/mymatches.html'
    context_object_name = 'my_matches_list'

    def get_queryset(self):
        return Match.objects.filter(Q(player1_id=self.request.user) | Q(player2_id=self.request.user)) \
            .filter(date__gt=timezone.now())\
            .order_by('tournament_id', 'date')

    def get_context_data(self, **kwargs):
        context = super(MyMatchesView, self).get_context_data(**kwargs)
        my_participations = Participation.objects.values_list('tournament_id').filter(user_id=self.request.user)
        context['tournaments'] = Tournament.objects.filter(id__in=my_participations)\
            .annotate(num_participants=Count('participation'))\
            .order_by('start_date')
        return context


class TournamentCreate(LoginRequiredMixin, FormView):
    template_name = 'tournaments/tournament_form.html'
    form_class = TournamentForm
    success_url = '/tournaments/sponsor/add/'

    def form_valid(self, form):
        form.instance.host_id = self.request.user
        is_valid = True
        if form.instance.max_number_of_participants < 2:
            form.add_error('max_number_of_participants', 'Tournament can be hosted only for 2 or more participants!')
            is_valid = False
        if is_valid:
            newTournament = form.save()
            self.request.session['tournament'] = newTournament.id
            return super().form_valid(form)
        return self.form_invalid(form)


class TournamentUpdate(UpdateView):
    form_class = TournamentForm
    model = Tournament
    success_url = '/tournaments/'


class JoinTournament(LoginRequiredMixin, FormView):
    template_name = 'tournaments/join_form.html'
    form_class = JoinForm
    success_url = '/tournaments/'

    def form_valid(self, form):
        form.instance.user_id = self.request.user
        form.instance.tournament_id = Tournament.objects.filter(id=self.request.session['tournament']).first()
        registration_set = Participation.objects\
            .filter(tournament_id=form.instance.tournament_id)
        participation_duplicate = registration_set\
            .filter(user_id=self.request.user)\
            .first()
        ranking_duplicate = registration_set\
            .filter(ranking=form.instance.ranking)\
            .first()
        license_duplicate = registration_set\
            .filter(license_number=form.instance.license_number)\
            .first()
        is_valid = True
        if participation_duplicate is not None:
            form.add_error(None, 'You participate in this tournament already!')
            is_valid = False
        if ranking_duplicate is not None:
            form.add_error('ranking', 'User with this ranking already registered for this tournament!')
            is_valid = False
        if license_duplicate is not None:
            form.add_error('license_number', 'User with this license number already registered for this tournament!')
            is_valid = False
        if len(registration_set) >= form.instance.tournament_id.max_number_of_participants:
            form.add_error(None, 'Tournament is already full!')
            is_valid = False
        if timezone.now() >= form.instance.tournament_id.registration_deadline:
            form.add_error(None, 'You can\'t register for this tournament anymore. It\'s after registration deadline.')
        if is_valid:
            form.save()
            return super().form_valid(form)
        else:
            return self.form_invalid(form)


def login_view(request):
    return render(request, 'tournaments/login.html')


def redirect_view(request):
    email = request.POST['Email']
    password = request.POST['password']
    user = authenticate(request, username=email, email=email, password=password)
    if user is not None:
        request.session['login_unsuccessful'] = False
        login(request, user)
        return redirect('tournaments:index')
    else:
        request.session['login_unsuccessful'] = True
        return redirect('tournaments:login')


def logout_view(request):
    logout(request)
    return redirect('tournaments:index')


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            subject = 'Activate your TournamentSite account.'
            current_site = get_current_site(request)
            message = render_to_string('tournaments/acc_activate_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': token_generator.make_token(user)
            })
            emailAddress = form.cleaned_data.get('email')
            mail = EmailMessage(subject, message, to=tuple([emailAddress]))
            mail.send()
            return render(request, 'tournaments/acc_activation_done.html', {'form': form})
    else:
        form = SignUpForm()
    return render(request, 'tournaments/signup.html', {'form': form})


def registration_finalized_view(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = MyUser.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, MyUser.DoesNotExist):
        user = None
    if user is not None and token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return render(request, 'tournaments/acc_activation_complete.html')
    else:
        return HttpResponse('Activation link is invalid!')


def logo_upload(request):
    ImageFormSet = modelformset_factory(Sponsor,
                                        form=SponsorForm, extra=10)
    # 'extra' means the number of photos that you can upload   ^
    if request.method == 'POST':
        formset = ImageFormSet(request.POST, request.FILES,
                               queryset=Sponsor.objects.none())

        if formset.is_valid():
            for form in formset.cleaned_data:
                # this helps to not crash if the user
                # do not upload all the photos
                if form:
                    logo = form['logo']
                    sponsor = Sponsor(logo=logo, tournament=Tournament.objects.filter(id=request.session['tournament']).first())
                    sponsor.save()
            return redirect('tournaments:index')
        else:
            print(formset.errors)
    else:
        formset = ImageFormSet(queryset=Sponsor.objects.none())
    return render(request, 'tournaments/sponsor_form.html',
                  {'formset': formset})
