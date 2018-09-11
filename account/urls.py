from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views
from .views import home, signup, signin, ask_question, answer, question_page, profile_page, vote, devote, bookmark, \
    unbookmark, share, unshare, comment, comment_devote, comment_vote

app_name = 'account'

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^signup/$', signup, name='signup'),
    url(r'^signin/$', signin, name='signin'),
    url(r'^ask/$', ask_question, name='ask'),
    url(r'^answer/$', answer, name='answer'),
    url(r'^question/(?P<q_id>\d+)/$', question_page, name='question'),
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


    url(r'^$', home, name='home'),
    # url(r'^', include('account.urls', namespace="account`")),
]