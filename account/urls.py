from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views
from .views import *

app_name = 'account'

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^edit_profile/$', model_form_upload, name='edit_profile'),
    url(r'^signup/$', signup, name='signup'),
    url(r'^signin/$', signin, name='signin'),
    url(r'^notifs-readall/$', read_all, name='readall'),
    url(r'^notifs-showall/$', all_notifs, name='showall'),
    url(r'^notifs-type_based/$', type_based_notifs, name='type_based_notifs'),
    url(r'^ask/$', ask_question, name='ask'),
    url(r'^search-topic/$', topic_search, name='topic_search'),
    url(r'^best_topic_based_users/(?P<t_id>\d+)/$', best_topic_based_users, name='best_topic_based_users'),
    url(r'^best_question_based_users/(?P<q_id>\d+)/$', best_question_based_users, name='best_question_based_users'),
    url(r'^answer/(?P<q_id>\d+)/$', answer, name='answer'),
    url(r'^question/(?P<q_id>\d+)/$', question_page, name='question'),
    url(r'^edit/(?P<q_id>\d+)/$', edit, name='edit'),
    url(r'^follow/(?P<q_id>\d+)/$', follow, name='follow'),
    url(r'^unfollow/(?P<q_id>\d+)/$', unfollow, name='unfollow'),
    url(r'^profile/(?P<u_id>\d+)/$', profile_page, name='profile'),
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
    url(r'^edit_full_name/(?P<u_id>\d+)/$', edit_full_name, name='edit_full_name'),
    url(r'^edit_main_credential/(?P<u_id>\d+)/$', edit_main_credential, name='edit_main_credential'),
    url(r'^edit_bio/(?P<u_id>\d+)/$', edit_bio, name='edit_bio'),

    url(r'^$', home, name='home'),
    # url(r'^', include('account.urls', namespace="account`")),
]