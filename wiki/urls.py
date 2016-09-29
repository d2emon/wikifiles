# coding: utf-8
from django.conf.urls import url
from django.views.generic.base import RedirectView
from wiki.views import PageView


urlpatterns = [
    url(r'^$', PageView.as_view(), name='wikiroot'),
    url(r'^(?P<path>.*)/__page.opt$', PageView.as_view(), name='opt'),
    url(r'^(?P<path>.*)/__page.wiki$', PageView.as_view(), name='wiki'),
    url(r'^(?P<path>.*)/__content.html$', PageView.as_view(), name='html'),
    # url(r'^(?P<path>.*)/__attach/(?P<file>.*)$', AttachView.as_view(), name='attach'),
    url(r'^(?P<path>.*)/$', RedirectView.as_view(pattern_name='wiki')),
    url(r'^__page.wiki$', RedirectView.as_view(pattern_name='wikiroot')),
    # url(r'^__page.wiki$', PageView.as_view(), name='wiki_root'),
]
