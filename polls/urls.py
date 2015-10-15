from django.conf.urls import url, patterns

from . import views
from django.contrib import admin

admin.autodiscover()

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
    url(r'^(?P<pk>[0-9]+)/results/$', views.ResultsView.as_view(), name='results'),
    url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),
    url(r'^/ad_click/$', views.ad_click, name='ad_click'),
    url(r'^tag/(?P<tag_id>[0-9]+)/$', views.tag, name='tag'),
    url(r'^/tag/$', views.tag, name='tag'),
]