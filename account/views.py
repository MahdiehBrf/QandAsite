from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse

from account.forms import SignUpForm, QForm, AForm
from account.models import User, Question, Answer, AnswerComment


def home(request):
    if request.user.is_authenticated:
        return render(request, 'home.html', {'unread_count': request.user.notifications.unread().count(),
                                                   'notifications': request.user.notifications.all()
                                                   })
    else:
        return render(request, 'home.html')


def ask_question(request):
    if request.method == 'POST':
        uf = QForm(request.POST)
        if uf.is_valid():
            question = uf.save(commit=False)
            question.asker = request.user
            question.save()

        else:
            print()
    else:
        form = QForm()
        return render(request, 'editortest.html', {'form': form,
                                                   'unread_count': request.user.notifications.unread().count(),
                                                   'notifications': request.user.notifications.all()
                                                   })


def edit(request, q_id):
    if request.method == 'POST':
        uf = QForm(request.POST, instance=Question.objects.get(id=q_id))
        if uf.is_valid():
            question = uf.save()
            return HttpResponseRedirect(reverse('account:question', args={q_id}))
        else:
            print()


def answer(request, q_id):
    if request.method == 'POST':
        uf = AForm(request.POST)
        if uf.is_valid():
            answer_f = uf.save(commit=False)
            answer_f.responder = request.user
            answer_f.question = Question.objects.get(id=q_id)
            answer_f.save()
            return render(request, 'answer.html', {'answer': answer_f, 'way': 'single'})
        else:
            print()


def signup(request):
    if request.method == 'POST':
        uf = SignUpForm(request.POST)
        if uf.is_valid():
            info = uf.instance
            user = User.objects.create_user(info.email, info.password, info.first_name, info.last_name)
            user.save()
            return HttpResponseRedirect(reverse('account:home'))


def signin(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('account:home'))


def question_page(request, q_id):
    question = Question.objects.get(id=q_id)
    return render(request, 'question.html', {'question': question})


def profile_page(request, u_id):
    user = User.objects.get(id=u_id)
    return render(request, 'profile.html', {'user': user})


def vote(request, a_id):
    selected_answer = Answer.objects.get(id=a_id)
    selected_answer.voters.add(request.user)
    return JsonResponse({'vote_count': selected_answer.voters.all().count()})


def devote(request, a_id):
    selected_answer = Answer.objects.get(id=a_id)
    selected_answer.voters.remove(request.user)
    return JsonResponse({'vote_count': selected_answer.voters.all().count()})


def comment_vote(request, c_id):
    selected_comment = AnswerComment.objects.get(id=c_id)
    selected_comment.voters.add(request.user)
    return JsonResponse({'vote_count': selected_comment.voters.all().count()})


def comment_devote(request, c_id):
    selected_comment = AnswerComment.objects.get(id=c_id)
    selected_comment.voters.remove(request.user)
    return JsonResponse({'vote_count': selected_comment.voters.all().count()})


def bookmark(request, a_id):
    selected_answer = Answer.objects.get(id=a_id)
    selected_answer.bookmarkers.add(request.user)
    return JsonResponse({})


def unbookmark(request, a_id):
    selected_answer = Answer.objects.get(id=a_id)
    selected_answer.bookmarkers.remove(request.user)
    return JsonResponse({})


def share(request, a_id):
    selected_answer = Answer.objects.get(id=a_id)
    selected_answer.shareholders.add(request.user)
    return JsonResponse({})


def unshare(request, a_id):
    selected_answer = Answer.objects.get(id=a_id)
    selected_answer.shareholders.remove(request.user)
    return JsonResponse({})


def comment(request, a_id):
    selected_answer = Answer.objects.get(id=a_id)
    text = request.GET['text']
    new_comment = AnswerComment(commenter=request.user, answer=selected_answer, text=text )
    new_comment.save()
    return render(request, 'comment.html', {'comment': new_comment})


def comment_delete(request, c_id):
    selected_comment = AnswerComment.objects.get(id=c_id)
    if request.user == selected_comment.commenter:
        selected_comment.delete()
    return JsonResponse({})


def answer_delete(request, a_id):
    selected_answer = Answer.objects.get(id=a_id)
    if request.user == selected_answer.responder:
        selected_answer.delete()
    return JsonResponse({})


def answer_edit(request, a_id):
    if request.method == 'POST':
        selected_answer = Answer.objects.get(id=a_id)
        if request.user == selected_answer.responder:
            selected_answer.text = request.POST['cke-'+a_id]
            selected_answer.save()
        return render(request, 'answer.html', {'answer': selected_answer, 'way': 'single'})


def follow(request, q_id):
    selected_question = Question.objects.get(id=q_id)
    selected_question.followers.add(request.user)
    return JsonResponse({'follower_count': selected_question.followers.all().count()})


def unfollow(request, q_id):
    selected_question = Question.objects.get(id=q_id)
    selected_question.followers.remove(request.user)
    return JsonResponse({'follower_count': selected_question.followers.all().count()})
