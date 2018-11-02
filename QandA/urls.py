from django.conf.urls import url
from .views import *

app_name = 'QandA'

urlpatterns = [
    url(r'^$', home, name='home'),
    url(r'^ask/$', ask_question, name='ask'),
    url(r'^best_topic_based_users/(?P<t_id>\d+)/$', best_topic_based_users, name='best_topic_based_users'),
    url(r'^best_topic_based_users/(?P<t_id>\d+)/(?P<q_id>\d+)/$', best_topic_based_users_for_question, name='best_topic_based_users_for_question'),
    url(r'^best_question_based_users/(?P<q_id>\d+)/$', best_question_based_users, name='best_question_based_users'),
    url(r'^answer/(?P<q_id>\d+)/$', answer, name='answer'),
    url(r'^question_topic/(?P<q_id>\d+)/$', question_topic, name='question_topic'),
    url(r'^question/(?P<q_id>\d+)/$', question_page, name='question'),
    url(r'^edit/(?P<q_id>\d+)/$', edit, name='edit'),
    url(r'^follow/(?P<q_id>\d+)/$', follow, name='follow'),
    url(r'^unfollow/(?P<q_id>\d+)/$', unfollow, name='unfollow'),
    url(r'^vote/(?P<a_id>\d+)/$', vote, name='vote'),
    url(r'^devote/(?P<a_id>\d+)/$', devote, name='devote'),
    url(r'^bookmark/(?P<a_id>\d+)/$', bookmark, name='bookmark'),
    url(r'^unbookmark/(?P<a_id>\d+)/$', unbookmark, name='unbookmark'),
    url(r'^share/(?P<a_id>\d+)/$', share, name='share'),
    url(r'^unshare/(?P<a_id>\d+)/$', unshare, name='unshare'),
    url(r'^comment/(?P<a_id>\d+)/$', comment, name='comment'),
    url(r'^comment_vote/(?P<c_id>\d+)/$', comment_vote, name='comment_vote'),
    url(r'^comment_devote/(?P<c_id>\d+)/$', comment_devote, name='comment_devote'),
    url(r'^comment_delete/(?P<c_id>\d+)/$', comment_delete, name='comment_delete'),
    url(r'^answer_delete/(?P<a_id>\d+)/$', answer_delete, name='answer_delete'),
    url(r'^answer_edit/(?P<a_id>\d+)/$', answer_edit, name='answer_edit'),
    url(r'^topic_delete/(?P<q_id>\d+)/(?P<t_id>\d+)/$', question_topic_delete, name='topic_delete'),
    url(r'^topic_add/(?P<q_id>\d+)/(?P<t_id>\d+)/$', question_topic_add, name='topic_add'),
    url(r'^answer_request/(?P<u_id>\d+)/(?P<q_id>\d+)/$', answer_request, name='answer_request'),
    url(r'^answer_add_credential/(?P<a_id>\d+)/(?P<c_id>\d+)/$', add_answer_credential, name='add_answer_credential'),

]