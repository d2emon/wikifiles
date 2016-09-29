# from django.db import models
import os
import configparser
import re


class WikiLink():
    def __init__(self, title="", root=""):
        self.title = title
        self.path = os.path.join(root, self.title)


class WikiPage():
    wiki_title = "Wiki"

    def __init__(self, root=""):
        self.root = root
        self.subpath = ""
        self.path = []

        self.opt = configparser.ConfigParser()
        self.text = ""
        self.html = ""

        self.children = []
        import logging
        logging.debug("Root:%s", self.root)

    def load(self, root=None, path=None):
        if root:
            self.root = root
        if path:
            self.subpath = path
        import logging
        logging.debug("Load:%s", self.root)

        # self.loadsub()
        # self.loadopt()
        # self.loadtxt()
        self.children = self.get_children_array()
        self.opt.read(self.get_filepath("__page.opt"))
        import logging
        for section in self.opt.sections():
            logging.debug("Section: %s", section)
            items = self.opt[section]
            for i in items:
                logging.debug("%s=%s", i, self.opt[section][i])

        self.text = self.load_file("__page.text")
        self.html = self.load_file("__content.html")

        # self.content = load_wiki(path, attach="{}{}__attach/".format(self.attach, subpath))

    def load_file(self, filename):
        try:
            filename = self.get_filepath(filename)
            if not os.path.isfile(filename):
                return False
            return open(filename, "r").read()
        except FileNotFoundError:
            return None

    def get_filepath(self, filename=""):
        return os.path.join(os.path.normpath(self.root), self.subpath, filename)

    def get_upper(self):
        return os.path.join(os.path.normpath(self.subpath), '..')

    def get_title(self):
        if not self.subpath:
            return self.wiki_title
        return os.path.basename(os.path.normpath(self.subpath))

    def get_children(self):
        import logging
        logging.debug("Root:%s", self.get_filepath())
        try:
            items = next(os.walk(self.get_filepath()))[1]
        except StopIteration:
            items = []
        logging.debug("Items:%s", items)
        items = list(filter(lambda f: not f.startswith('.') and not f.startswith('__'), items))
        items.sort()
        return items

    def get_children_array(self):
        return [WikiLink(c, self.subpath) for c in self.get_children()]

    def get_html(self, href=None, attach=None):
        href = r"/wiki/{}\1/__content.html".format(self.subpath)
        attach = r"/static/wiki/{}__attach/".format(self.subpath)

        found = re.search(r'<body>(.*)</body>', self.html, re.DOTALL)
        if not found:
            return _("Wiki {} not found. File {} is not exists.".format(self.get_filepath()))

        text = found.group(1)
        if href:
            text = re.sub(r'href="^(http[s?]\:)(.*?)"', r'href="{}"'.format(href), text)
        if attach:
            text = re.sub(r'="__attach/(.*?)"', r'="{}\1"'.format(attach), text)
        return text
