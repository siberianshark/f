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


app = Flask(__name__)


migrate = Migrate()
migrate.init_app(app, db)


@app.route("/")
def index():
    return render_template('index.html')


app.register_blueprint(users_app, url_prefix="/users")
app.register_blueprint(articles_app, url_prefix='/articles')
# app.config["SECRET_KEY"] = "abcdefg123456"
app.register_blueprint(auth_app, url_prefix="/auth")


cfg_name = os.environ.get("CONFIG_NAME") or "BaseConfig"
app.config.from_object(f"blog.configs.{cfg_name}")


# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"
# app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
login_manager.init_app(app)
db.init_app(app)