from django.urls import reverse
from django.views.generic import TemplateView, RedirectView
from wiki.models import WikiPage, WikiLink
import os


class PageView(TemplateView):
    template_name = 'wiki/page.html'
    path = "/windows/wiki/mywiki"  # settings.get('wiki', dict()).get('wiki_root', "/wiki/mywiki")
    attach = "web/wiki"    # settings.get('wiki', dict()).get('wiki_url', "/web/wiki/")

    def get_children(self, path):
        try:
            items = next(os.walk(path))[1]
        except StopIteration:
            items = []
        items = list(filter(lambda f: not f.startswith('.') and not f.startswith('__'), items))
        return items

    def get_context_data(self, **kwargs):
        subpath = kwargs.get('path', '')
        if subpath:
            subpath = os.path.normpath(subpath) + '/'
        path = os.path.join(self.path, subpath)

        p = os.path.normpath(subpath)
        crumbs = []
        while p:
            p, crumb = os.path.split(os.path.normpath(p))
            crumbs.append(WikiLink(crumb, p))
            if p == '/':
                break
        crumbs.reverse()
        crumbs.pop()

        w = WikiPage(root=self.path)
        w.root_url = reverse('wikiroot')
        w.load(path=subpath)

        context = super(PageView, self).get_context_data(**kwargs)
        context['crumbs'] = crumbs
        context['wiki'] = w
        return context


class HtmlView(PageView):
    template_name = 'wiki/html.html'


class AttachView(RedirectView):
    path = "/web/wiki/"  # settings.get('wiki', dict()).get('wiki_url', "/web/wiki/")

    def get_redirect_url(self, *args, **kwargs):
        subpath = kwargs.get('path', '')
        filename = kwargs.get('file', '')
        return os.path.join(self.path, subpath, '__attach', filename)
