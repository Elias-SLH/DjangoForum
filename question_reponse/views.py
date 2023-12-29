from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import logout as auth_logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from .forms import CustomUserCreationForm, QuestionForm, AnswerForm
from .models import Question, Answer
from .decorators import unauthenticated_user


class IndexView(generic.ListView):
    """Index page listing 7 questions by page"""
    paginate_by = 7
    template_name = 'qr/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Order questions from most recent to oldest"""
        return Question.objects.order_by('-pub_date')


@unauthenticated_user
def register_page(request):
    """
    Validate and save register form

    Redirect user to login page if registered successfully,
    otherwise keep rendering register page
    """
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully")
            return redirect('/login/')
    else:
        form = CustomUserCreationForm()

    return render(request, 'qr/register.html', {'form': form})


@unauthenticated_user
def login_page(request):
    """
    Authenticate user to log him in

    Redirect user to index page if logged in successfully,
    otherwise keep rendering login page"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('qr:index')
        else:
            messages.info(request, "Incorrect username or password")

    return render(request, 'qr/login.html')


def logout_user(request):
    """Log out user and redirect to login page"""
    logout(request)
    return redirect('qr:login')


@login_required(login_url='/login/')
def ask_question(request):
    """
    Validate and save question form

    Redirect user to question's detail if question submitted successfully,
    otherwise keep rendering question page
    """
    if request.method == 'POST':
        form = QuestionForm(request.POST)

        if form.is_valid():
            question = Question()
            question.topic = form.cleaned_data['topic']
            question.description = form.cleaned_data['description']
            question.user = request.user
            question.save()

            return redirect('qr:detail', question.id)
        else:
            print(form.errors)

    else:
        form = QuestionForm()

    return render(request, 'qr/question_form.html', {'form': form})


class QuestionDetailView(LoginRequiredMixin, generic.DetailView):
    """Question's detail page rendering the question and the related answers"""
    model = Question
    template_name = 'qr/detail.html'
    login_url = '/login/'

    form = AnswerForm

    def post(self, request, *args, **kwargs):
        """Validate and save answer form"""
        form = AnswerForm(request.POST)
        if form.is_valid():
            question = self.get_object()
            form.instance.user = request.user
            form.instance.question = question
            form.save()

            return redirect('qr:detail', question.id)

    def get_context_data(self, **kwargs):
        """Retrieve question, answers and up/down vote"""
        post_answer = Answer.objects.all().filter(question=self.object.id)
        question = get_object_or_404(Question, id=self.kwargs['pk'])
        upvoted = False
        if question.upvote.filter(id=self.request.user.id).exists():
            upvoted = True
        context = super().get_context_data(**kwargs)
        context.update({
            'form': self.form,
            'post_answer': post_answer,
            'post_answer_count': post_answer.count(),
            'question_upvotes': question.total_upvote(),
            'upvoted': upvoted,
        })
        return context


@login_required(login_url='/login/')
def vote(request, pk):
    """Allow user to upvote/downvote other's questions"""
    question = get_object_or_404(Question, id=request.POST.get('question_upvote_id'))
    if question.upvote.filter(id=request.user.id).exists():
        question.upvote.remove(request.user)
    else:
        question.upvote.add(request.user)

    return redirect('qr:detail', question.id)


def search(request):
    """Search question based on keyword in questions's topic"""
    if request.method == 'POST':
        searched = request.POST.get('searched')
        questions = Question.objects.filter(topic__icontains=searched)
        return render(request, 'qr/search.html', {'searched': searched, 'questions': questions})
    else:
        return render(request, 'qr/search.html', {})


@login_required(login_url='/login/')
def profile(request):
    """Display user's questions and answers"""
    questions = Question.objects.filter(user_id=request.user)
    answers = Answer.objects.filter(user_id=request.user)
    context = {'questions': questions, 'answers': answers}
    return render(request, 'qr/profile.html', context)


class UpdateQuestion(LoginRequiredMixin, generic.UpdateView):
    """Page to update question"""
    model = Question
    form_class = QuestionForm
    template_name = 'qr/edit_question.html'
    login_url = '/login/'


class DeleteQuestion(LoginRequiredMixin, generic.DeleteView):
    """Page to delete question"""
    model = Question
    template_name = 'qr/delete_question.html'
    success_url = reverse_lazy('qr:index')
    login_url = '/login/'


class UpdateAnswer(LoginRequiredMixin, generic.UpdateView):
    """Page to update answer"""
    model = Answer
    form_class = AnswerForm
    template_name = 'qr/edit_answer.html'
    login_url = '/login/'


class DeleteAnswer(LoginRequiredMixin, generic.DeleteView):
    """Page to delete answer"""
    model = Answer
    template_name = 'qr/delete_answer.html'
    success_url = reverse_lazy('qr:index')
    login_url = '/login/'


@login_required(login_url='/login/')
def disable_user(request, pk):
    """
    Allow user to disable his account

    Redirect to login page
    """
    user = request.user
    user.is_active = False
    user.save()
    auth_logout(request)
    messages.success(request, 'Profile successfully disabled. Contact admin to reactivate it.')

    return redirect('qr:login')
