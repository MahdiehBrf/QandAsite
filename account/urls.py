from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views
from .views import *

app_name = 'account'

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^signup/$', signup, name='signup'),
    url(r'^signin/$', signin, name='signin'),
    url(r'^notifs-readall/$', read_all, name='readall'),
    url(r'^notifs-showall/$', all_notifs, name='showall'),
    url(r'^notifs-type_based/$', type_based_notifs, name='type_based_notifs'),
    url(r'^search-topic/$', topic_search, name='topic_search'),
    url(r'^profile/(?P<u_id>\d+)/$', profile_page, name='profile'),
    url(r'^edit_full_name/(?P<u_id>\d+)/$', edit_full_name, name='edit_full_name'),
    url(r'^edit_main_credential/(?P<u_id>\d+)/$', edit_main_credential, name='edit_main_credential'),
    url(r'^edit_bio/(?P<u_id>\d+)/$', edit_bio, name='edit_bio'),
    url(r'^edit_avatar/$', edit_profile_avatar, name='edit_avatar'),
    url(r'^add_credential/(?P<c_type>\w+)/$', add_credential, name='add_credential'),
    url(r'^topic_all/$', topic_all, name='topic_all'),
    url(r'^user_credentials_all/$', user_credentials_all, name='user_credentials_all'),
    url(r'^profile_get_feed/(?P<u_id>\d+)/(?P<f_type>\w+)/$', profile_get_feed, name='profile_get_feed'),
    url(r'^follow_topic/(?P<t_id>\d+)/$', follow_topic, name='topic_follow'),
    url(r'^follow_user/(?P<u_id>\d+)/$', follow_user, name='user_follow'),
    url(r'^topic_page/(?P<t_id>\d+)/$', topic_page, name='topic_page'),

]