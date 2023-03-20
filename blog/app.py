from blog.models.database import db
from flask import Flask, render_template
# from flask import request
# from werkzeug.exceptions import BadRequest
from blog.views.users import users_app
from blog.views.articles import articles_app
from blog.models import User
from blog.views.auth import login_manager, auth_app
import os
from flask_migrate import Migrate
from blog.security import flask_bcrypt
from blog.views.authors import authors_app
from blog.admin import admin
from blog.api import init_api


app = Flask(__name__)


migrate = Migrate()
migrate.init_app(app, db)


flask_bcrypt.init_app(app)


@app.route("/")
def index():
    return render_template('index.html')


app.register_blueprint(users_app, url_prefix="/users")
app.register_blueprint(articles_app, url_prefix='/articles')
app.register_blueprint(authors_app, url_prefix="/authors")

# app.config["SECRET_KEY"] = "abcdefg123456"
app.register_blueprint(auth_app, url_prefix="/auth")


cfg_name = os.environ.get("CONFIG_NAME") or "BaseConfig"
app.config.from_object(f"blog.configs.{cfg_name}")


# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"
# app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
login_manager.init_app(app)
db.init_app(app)
admin.init_app(app)
api = init_api(app)


@app.cli.command("create-admin")
def create_admin():
    """
    Run in your terminal:
    ➜ flask create-admin
    > created admin: <User #1 'admin'>
    """
    admin = User(username="Admin", email="Admin@Admin.com", is_staff=True)
    admin.password = os.environ.get("ADMIN_PASSWORD") or "adminpass"
    db.session.add(admin)
    db.session.commit()
    print("created admin:", admin)

@app.cli.command("create-tags")
def create_tags():
    """
    Run in your terminal:
    ➜ flask create-tags
    """
    from blog.models import Tag
    for name in [
        "flask",
        "django",
        "python",
        "sqlalchemy",
        "news",
    ]:
        tag = Tag(name=name)
        db.session.add(tag)
    db.session.commit()
print("created tags")
