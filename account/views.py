from django.contrib.auth import authenticate, login
from django.core.files.storage import FileSystemStorage
from django.db.models import Count
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
import json
from django.views.decorators.csrf import csrf_exempt


from account.forms import *
from account.models import User, Question, Answer, AnswerComment, NOTIF_TYPE, Topic, AnswerRequest, MainCredential, \
    Credential


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
            return HttpResponseRedirect(reverse('account:question', args={question.id}))
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
            question = uf.save(commit=False)
            # if request.user not in question.editors.all():
            question.editors.add(request.user)
            question.save()
            return HttpResponseRedirect(reverse('account:question', args={q_id}))
        else:
            print()


def answer(request, q_id):
    if request.method == 'POST':
        answer_f = Answer()
        answer_f.responder = request.user
        answer_f.text = request.POST['ckeq-'+q_id]
        answer_f.question = Question.objects.get(id=q_id)
        answer_f.save()
        return render(request, 'answer.html', {'answer': answer_f, 'way': 'single'})


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
    return render(request, 'profile.html', {'selected_user': user})


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
            selected_answer.text = request.POST['ckea-'+a_id]
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


def read_all(request):
    request.user.notifications.mark_all_as_read()
    return JsonResponse({})


def all_notifs(request):
    all_notifs = request.user.notifications.all()
    return render(request, 'notifications.html', {'notifs': all_notifs})


def type_based_notifs(request):
    type = request.GET['type']
    cond = json.dumps({'type': type})[1:-1].replace(" ", "")
    notifs = request.user.notifications.filter(data__contains=cond)
    return render(request, 'notif.html', {'notifs': notifs})


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


def topic_search(request):
    name = request.GET['name']
    way = request.GET['way']
    topics = Topic.objects.filter(name__contains=name)
    if way == 'summary':
        return render(request, 'topic_list.html', {'topics': topics, 'way': 'summary'})
    else:
        return render(request, 'topic_list.html', {'topics': topics, 'way': 'full', 'selected_user': request.user})


def best_topic_based_users(request, t_id, q_id):
    question = Question.objects.get(id=q_id)
    topic = Topic.objects.get(id=t_id)
    user_subtract_set = AnswerRequest.objects.filter(asker=request.user, question=question).values_list('askee', flat=True)
    user_count = get_user_count(topic, user_subtract_set, request.user)
    return render(request, 'user_answer_counts.html', {'user_count':user_count, 'topic':topic})


def get_user_count(topic, user_subtract_set, asker):
    answers = topic.questions.values_list('answer', flat=True)
    users = Answer.objects.filter(id__in=answers).values('responder').order_by()
    user_count = users.annotate(answer_count=Count('responder')).order_by('-answer_count')[:20]
    users = User.objects.filter(id__in=user_count.values_list('responder', flat=True)).exclude(id__in=user_subtract_set).exclude(id=asker.id)
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
    return render(request, 'user_topic_answer_counts.html', {'user_topic_count': user_topic_count})


def answer_request(request, u_id, q_id):
    question = Question.objects.get(id=q_id)
    user = User.objects.get(id=u_id)
    ar = AnswerRequest(asker=request.user, askee=user, question=question)
    ar.save()
    return JsonResponse({})


def model_form_upload(request):
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('account:profile', args={request.user.id}))
    else:
        form = UserForm()
    return render(request, 'edit_profile.html', {
        'form': form
    })


def edit_full_name(request, u_id):
    first_name = request.GET['first_name']
    last_name = request.GET['last_name']
    selected_user = User.objects.get(id=u_id)
    if request.user == selected_user:
        selected_user.first_name = first_name
        selected_user.last_name = last_name
        selected_user.save()
    return JsonResponse({})


def edit_main_credential(request, u_id):
    text = request.GET['text']
    selected_user = User.objects.get(id=u_id)
    if request.user == selected_user:
        main_credential = MainCredential(user=selected_user, text=text)
        main_credential.save()
    return JsonResponse({})


def edit_bio(request, u_id):
    if request.method == 'POST':
        selected_user = User.objects.get(id=u_id)
        if request.user == selected_user:
            selected_user.bio = request.POST['bio']
            selected_user.save()
            return HttpResponseRedirect(reverse('account:profile', args={selected_user.id}))


def add_answer_credential(request, a_id, c_id):
    selected_answer = Answer.objects.get(id=a_id)
    selected_credential = Credential.objects.get(id=c_id)
    if request.user == selected_answer.responder:
        selected_answer.credential = selected_credential
        selected_answer.save()
    return JsonResponse({})


@csrf_exempt
def add_credential(request, c_type):
    uf = None
    if c_type == 'employment':
        uf = EmploymentForm(request.POST)
    elif c_type == 'education':
        uf = EducationForm(request.POST)
    elif c_type == 'location':
        uf = LocationForm(request.POST)
    elif c_type == 'language':
        uf = LanguageForm(request.POST)
    elif c_type == 'experience':
        uf = ExperienceForm(request.POST)
    if uf.is_valid():
        credential = uf.save(commit=False)
        credential.user = request.user
        credential.save()
        return render(request, 'credential_item.html', {'type': c_type, 'credential': credential})


def topic_all(request):
    topics = {}
    for topic in Topic.objects.all():
        topics[topic.id] = topic.name
    return JsonResponse({'topics': topics})


def user_credentials_all(request):
    return render(request, 'profile_credential-bar.html', {'selected_user': request.user})


def profile_get_feed(request, u_id, f_type):
    selected_user = User.objects.get(id=u_id)
    if f_type == 'answers':
        return render(request, 'answers.html', {'answers': selected_user.answer_set})
    elif f_type == 'questions':
        return render(request, 'questions.html', {'questions': selected_user.question_set})
    elif f_type == 'shares':
        return render(request, 'answers.html', {'answers': selected_user.shares})
    elif f_type == 'followings':
        return render(request, 'user_list.html', {'users': selected_user.followees})
    elif f_type == 'followers':
        return render(request, 'user_list.html', {'users': selected_user.followers})
    elif f_type == 'usertopics':
        return render(request, 'topic_list.html', {'topics': selected_user.topics, 'way': 'full', 'selected_user':selected_user})
    elif f_type == 'bookmarks':
        if request.user == selected_user:
            return render(request, 'answers.html', {'answers': selected_user.bookmarks})
    elif f_type == 'topquestions':
        if request.user == selected_user:
            if request.user.first_login:
                request.user.first_login = False
                request.user.save()
            questions = None
            for topic in selected_user.topics.all():
                if questions is None:
                    questions = topic.questions.all()
                else:
                    questions = questions | topic.questions.all()
            best_questions = None
            last_questions = None
            if questions:
                best_questions = questions.annotate(follower_count=Count('followers'), answer_count=Count('answer')).order_by('-follower_count', 'answer_count')
                if best_questions.count() < 20:
                    last_questions = Question.objects.exclude(id__in=best_questions).order_by('-pub_date')[:20-best_questions.count()]
            else:
                last_questions = Question.objects.order_by('-pub_date')[:20]

            return render(request, 'questions.html', {'user_questions': best_questions, 'questions': last_questions})
    elif f_type == 'topanswers':
        if request.user == selected_user:
            answers = None
            for topic in selected_user.topics.all():
                topic_answers = Answer.objects.filter(id__in=topic.questions.values('answer'))
                if answers is None:
                    answers = topic_answers
                else:
                    answers = answers | topic_answers.all()
            best_answers = None
            top_answers = None
            if answers:
                best_answers = answers.annotate(share_count=Count('shareholders'), vote_count=Count('voters'),
                                                bookmark_count=Count('bookmarkers')).order_by('-vote_count',
                                                                                              '-share_count',
                                                                                              '-bookmark_count')
                if best_answers.count() < 20:
                    top_answers = Answer.objects.exclude(id__in=best_answers).annotate(share_count=Count('shareholders'), vote_count=Count('voters'),
                                                bookmark_count=Count('bookmarkers')).order_by('-vote_count',
                                                                                              '-share_count',
                                                                                              '-bookmark_count')[:20-best_answers.count()]
            else:
                top_answers = Answer.objects.annotate(share_count=Count('shareholders'), vote_count=Count('voters'),
                                                bookmark_count=Count('bookmarkers')).order_by('-vote_count',
                                                                                              '-share_count',
                                                                                              '-bookmark_count')[:20]

            return render(request, 'answers.html', {'user_answers': best_answers, 'answers': top_answers})
    elif f_type == 'addtopics':
        if request.user == selected_user:
            return render(request, 'all-topics.html', {'topics': Topic.objects.all()})
    elif f_type == 'requests':
        if request.user == selected_user:
            requests = AnswerRequest.objects.filter(askee=selected_user)
            return render(request, 'requests.html', {'requests': requests})


def topic_image_upload(request, t_id):
    if request.method == 'POST':
        selected_topic = Topic.objects.get(id=t_id)
        form = TopicForm(request.POST, request.FILES, instance=selected_topic)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('account:home'))
    else:
        form = TopicForm()
    return render(request, 'edit_topic.html', {
        'form': form
    })


def follow_topic(request, t_id):
    is_follow = int(request.GET['follow'])
    selected_topic = Topic.objects.get(id=t_id)
    if is_follow == 1:
        request.user.topics.add(selected_topic)
    else:
        request.user.topics.remove(selected_topic)
    return JsonResponse({'count': selected_topic.followers.count(), 'name': selected_topic.name, 'url': selected_topic.image.url})


def follow_user(request, u_id):
    is_follow = int(request.GET['follow'])
    selected_user = User.objects.get(id=u_id)
    if is_follow == 1:
        request.user.followees.add(selected_user)
    else:
        request.user.followees.remove(selected_user)
    return JsonResponse({'count': selected_user.followers.count()})


def question_topic(request, q_id):
    topics = Question.objects.get(id=q_id).topics
    return render(request, 'topic_list.html', {'topics': topics, 'way': 'empty'})