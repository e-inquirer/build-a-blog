import webapp2
import jinja2
import os

from google.appengine.ext import db

# set up jinja2
template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir))


class Handler (webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

class Art(db.Model):
    title = db.StringProperty(required = True)
    art = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)

class MainPage(Handler):
    def get(self):
        self.redirect("/blog")

class Blog(Handler):
    def render_front(self, title="", art="", error=""):
        arts = db.GqlQuery("SELECT * FROM Art ORDER BY created DESC LIMIT 5")

        self.render("blog.html", title=title, art=art, error=error, arts=arts)

    def get(self):
        self.render_front()

class NewPost(Handler):
    def render_front(self, title="", art="", error=""):
        self.render("newpost.html", title=title, art=art, error=error)

    def get(self):
        self.render_front()
            
    def post(self):
        title = self.request.get("title")
        art = self.request.get("art")

        if title and art:
            a = Art(title = title, art = art)
            a.put()

            self.redirect("/blog")

        else:
            error = "we need both, a title and some Artwork!"
            self.render_front(title, art, error)

class ViewPostHandler(webapp2.RequestHandler):
    def get(self, id):
        pass #replace this with some code to handle the request


# Route handlers
app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/blog', Blog),
    ('/newpost', NewPost),
    webapp2.Route('/blog/<id:\d+>', ViewPostHandler)
], debug=True)
