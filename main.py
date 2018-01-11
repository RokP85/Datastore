#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import jinja2
import webapp2
from models import Sporocilo

#           "GC_GET2/templates"
#       "GC_GET2"
template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=False)


class BaseHandler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        return self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        return self.write(self.render_str(template, **kw))

    def render_template(self, view_filename, params=None):
        if params is None:
            params = {}
        template = jinja_env.get_template(view_filename)
        return self.response.out.write(template.render(params))


class MainHandler(BaseHandler):
    def get(self):
        return self.render_template("hello.html")

class IzpisHandler(BaseHandler):
    def get(self):
        komentarji = Sporocilo.query().fetch()
        params = {"vnosi": komentarji}
        return self.render_template("vnosi.html", params=params)

    def post(self):
        ime = raw_input(self.request.get("ime"))
        priimek = raw_input(self.request.get("priimek"))
        email = raw_input(self.request.get("email"))
        sporocilo = raw_input(self.request.get("sporocilo"))

        nov_komentar = Sporocilo(ime=ime, priimek=priimek, email=email, sporocilo=sporocilo)
        nov_komentar.put()

        self.write(nov_komentar)


class PodrobnostiHandler(BaseHandler):
    def get(self, sporocilo_id):

        nov_komentar = Sporocilo.get_by_id(int(sporocilo_id))

        params  = {"sporocilo": nov_komentar}

        return self.write(nov_komentar)

app = webapp2.WSGIApplication([
    webapp2.Route("/", MainHandler),
    webapp2.Route("/izpis", IzpisHandler),
    webapp2.Route("/podrobnosti/<sporocilo_id:\d+>", PodrobnostiHandler)
], debug=True)
