from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from .models import Question, Choice, Vote
from django.template import loader
from django.urls import reverse
from django.views import generic
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, authenticate, update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.http import Http404

from .forms import UserLoginForm, UserRegistrationForm, UserEditForm, QuestionForm

from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy

def basic(request):
    return render(request, 'polls/basic.html')

def login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user:
                auth.login(request, user)
                return HttpResponseRedirect(reverse('polls:index'))
    else:
        form = UserLoginForm()
    context = {'form': form}
    return render(request, 'polls/login.html', context)

@login_required
def userlogout(request):
    logout(request)
    return HttpResponseRedirect(reverse('polls:login'))

@login_required
def profile(request):
    user = request.user
    context = {
        'user': user,
    }
    return render(request, 'polls/profile.html', context)

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('polls:login'))
    else:
        form = UserRegistrationForm()
    context = {'form': form}
    return render(request, 'polls/register.html', context)

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = UserEditForm(data=request.POST, files=request.FILES, instance=request.user)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return HttpResponseRedirect(reverse('polls:profile'))
    else:
        form = UserEditForm(instance=request.user)
    context = {'form': form}
    return render(request, 'polls/profile_edit.html', context)

class PasswordChange(LoginRequiredMixin, PasswordChangeView):
  template_name = 'polls/password_change.html'
  success_url = reverse_lazy('polls:profile')

  def form_valid(self, form):
    user = form.save()
    update_session_auth_hash(self.request, user)
    return super().form_valid(form)

@login_required
def delete_profile(request):
  user = request.user
  if request.method == 'POST':
    user.delete()
    logout(request)
    return HttpResponseRedirect(reverse('basic'))
  else:
    context = {'user': user}
    return render(request, 'polls/profile_delete.html', context)


class IndexView(LoginRequiredMixin, generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        return Question.objects.filter(expiration_date__gte=timezone.now()).order_by('-pub_date')

class DetailView(LoginRequiredMixin, generic.DetailView):
  model = Question
  template_name = 'polls/detail.html'

  def get_object(self, queryset=None):
      question = super().get_object(queryset)
      if not question.is_active():
          raise Http404("Вопрос недоступен.")  # обработка недоступного вопроса
      return question

class ResultsView(LoginRequiredMixin, generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        question = self.object
        total_votes = sum(choice.votes for choice in question.choice_set.all())

        # Создаём список с кортежами (выбор, процент)
        choices_with_percentages = []
        for choice in question.choice_set.all():
            choice_percentage = (choice.votes / total_votes * 100) if total_votes > 0 else 0
            choices_with_percentages.append((choice, choice_percentage))

        context['choices_with_percentages'] = choices_with_percentages
        return context


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    user = request.user

    if Vote.objects.filter(user=user, question=question).exists():
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': 'Вы уже проголосовали за этот вопрос.'
        })
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': 'Вы не сделали выбор.'
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()

        Vote.objects.create(user=user, question=question, choice=selected_choice, voted=True)

        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

def create_question(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST, request.FILES)
        if form.is_valid():
            question = form.save(commit=False)
            question.pub_date = timezone.now()
            question.save()
            choice_texts = form.cleaned_data['choices'].split(',')
            for choice_text in choice_texts:
                Choice.objects.create(question=question, choice_text=choice_text.strip())
            return HttpResponseRedirect(reverse('polls:index'))
    else:
        form = QuestionForm()
    return render(request, 'polls/create_question.html', {'form': form})