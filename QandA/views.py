from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse

from QandA.forms import *
from account.models import User, Credential, Topic
from QandA.models import Question, Answer, AnswerComment, AnswerRequest


@login_required
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
            return HttpResponseRedirect(reverse('QandA:question', args={question.id}))
        else:
            print()


def edit(request, q_id):
    if request.method == 'POST':
        uf = QForm(request.POST, instance=Question.objects.get(id=q_id))
        if uf.is_valid():
            question = uf.save(commit=False)
            # if request.user not in question.editors.all():
            question.editors.add(request.user)
            question.save()
            return HttpResponseRedirect(reverse('QandA:question', args={q_id}))
        else:
            print()


def answer(request, q_id):
    if request.method == 'POST':
        answer_f = Answer()
        answer_f.responder = request.user
        answer_f.text = request.POST['ckeq-'+q_id]
        answer_f.question = Question.objects.get(id=q_id)
        answer_f.save()
        return render(request, 'Answer/answer.html', {'answer': answer_f, 'way': 'single'})


def question_page(request, q_id):
    question = Question.objects.get(id=q_id)
    return render(request, 'Question/question.html', {'question': question})


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
    return render(request, 'Comment/comment.html', {'comment': new_comment})


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
            selected_answer.text = request.POST['ckea-'+a_id]
            selected_answer.save()
        return render(request, 'Answer/answer.html', {'answer': selected_answer, 'way': 'single'})


def follow(request, q_id):
    selected_question = Question.objects.get(id=q_id)
    selected_question.followers.add(request.user)
    return JsonResponse({'follower_count': selected_question.followers.all().count()})


def unfollow(request, q_id):
    selected_question = Question.objects.get(id=q_id)
    selected_question.followers.remove(request.user)
    return JsonResponse({'follower_count': selected_question.followers.all().count()})


def question_topic_delete(request, q_id, t_id):
    selected_question = Question.objects.get(id=q_id)
    selected_topic = Topic.objects.get(id=t_id)
    selected_question.topics.remove(selected_topic)
    return JsonResponse({})


def question_topic_add(request, q_id, t_id):
    selected_question = Question.objects.get(id=q_id)
    selected_topic = Topic.objects.get(id=t_id)
    included = 0
    if selected_topic in selected_question.topics.all():
        included = 1
    else:
        selected_question.topics.add(selected_topic)
    return JsonResponse({'topic_id': selected_topic.id, 'topic_name': selected_topic.name, 'included': included})


def best_topic_based_users_for_question(request, t_id, q_id):
    question = Question.objects.get(id=q_id)
    topic = Topic.objects.get(id=t_id)
    user_subtract_set = AnswerRequest.objects.filter(asker=request.user, question=question).values_list('askee', flat=True)
    user_count = get_user_count(topic, user_subtract_set, request.user)
    return render(request, 'Request/user_answer_counts.html', {'user_count':user_count, 'topic':topic})


def best_topic_based_users(request, t_id):
    topic = Topic.objects.get(id=t_id)
    user_count = get_user_count(topic)
    return render(request, 'User/best_topic_based_users.html', {'user_count': user_count})


def get_user_count(topic, user_subtract_set=None, asker=None):
    answers = topic.questions.values_list('answer', flat=True)
    users = Answer.objects.filter(id__in=answers).values('responder').order_by()
    user_count = users.annotate(answer_count=Count('responder')).order_by('-answer_count')[:20]
    if user_subtract_set and asker:
        users = User.objects.filter(id__in=user_count.values_list('responder', flat=True)).exclude(id__in=user_subtract_set).exclude(id=asker.id)
    else:
        users = User.objects.filter(id__in=user_count.values_list('responder', flat=True))
    counts = user_count.values_list('answer_count', flat=True)
    return zip(users, counts)


def best_question_based_users(request, q_id):
    question = Question.objects.get(id=q_id)
    user_topic_count = {}
    user_subtract_set = AnswerRequest.objects.filter(asker=request.user, question=question).values_list('askee', flat=True)
    for topic in question.topics.all():
        user_count = get_user_count(topic, user_subtract_set, request.user)
        for user, count in user_count:
            if user not in user_topic_count:
                user_topic_count[user] = {}
            user_topic_count[user][topic] = count
    return render(request, 'Request/user_topic_answer_counts.html', {'user_topic_count': user_topic_count})


def answer_request(request, u_id, q_id):
    question = Question.objects.get(id=q_id)
    user = User.objects.get(id=u_id)
    ar = AnswerRequest(asker=request.user, askee=user, question=question)
    ar.save()
    return JsonResponse({})


def add_answer_credential(request, a_id, c_id):
    selected_answer = Answer.objects.get(id=a_id)
    selected_credential = Credential.objects.get(id=c_id)
    if request.user == selected_answer.responder:
        selected_answer.credential = selected_credential
        selected_answer.save()
    return JsonResponse({})


def question_topic(request, q_id):
    topics = Question.objects.get(id=q_id).topics
    return render(request, 'Topic/topic_list.html', {'topics': topics, 'way': 'empty'})
