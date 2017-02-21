import webapp2, jinja2, os
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
    def render_front(self, title="", art="", error=""):
        arts = db.GqlQuery("SELECT * FROM Art ORDER BY created DESC")

        self.render("front.html", title=title, art=art, error=error, arts=arts)

    def get(self):
        #self.render("front.html")
        self.render_front()

    def post(self):
        title = self.request.get("title")
        art = self.request.get("art")

        if title and art:
            #self.write("Thanks!")
            a = Art(title = title, art = art)
            a.put()

            self.redirect("/")

        else:
            error = "we need both, a title and some Artwork!"
            self.render_front(title, art, error)

# Route handlers
app = webapp2.WSGIApplication([
    ('/', MainPage)
    ('/blog', Blog)
    ('/blog/newpost', NewPost)
], debug=True)

