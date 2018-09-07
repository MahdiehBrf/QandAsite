from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views
from .views import home, signup, signin, editor, answer, question_page

app_name = 'account'

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^signup/$', signup, name='signup'),
    url(r'^signin/$', signin, name='signin'),
    url(r'^editor/$', editor, name='editor'),
    url(r'^answer/$', answer, name='answer'),
    url(r'^question/(?P<q_id>\d+)/$', question_page, name='question'),

    url(r'^$', home, name='home'),
    # url(r'^', include('account.urls', namespace="account`")),
]