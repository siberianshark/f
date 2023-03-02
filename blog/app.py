from flask import Flask, render_template
from flask import request
from werkzeug.exceptions import BadRequest
from blog.views.users import users_app
from blog.views.articles import articles_app


app = Flask(__name__)


@app.route("/")
def index():
    return render_template('index.html')


app.register_blueprint(users_app, url_prefix="/users")
app.register_blueprint(articles_app, url_prefix='/articles')