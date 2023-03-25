from flask import Blueprint, render_template, request, redirect, url_for, current_app
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from blog.models import User
import blog
from sqlalchemy.exc import IntegrityError
from blog.models.database import db
from werkzeug.exceptions import NotFound
from blog.forms.user import RegistrationForm, LoginForm
from werkzeug.utils import secure_filename

auth_app = Blueprint("auth_app", __name__)
login_manager = LoginManager()
login_manager.login_view = "auth_app.login"

@auth_app.route("/login/", methods=["GET", "POST"], endpoint="login")
def login():
    if current_user.is_authenticated:
        return redirect("/")
    form = LoginForm(request.form)
    if request.method == "POST" and form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).one_or_none()
        if user is None:
            return render_template("auth/login.html", form=form, error="username doesn't exist")
        if not user.validate_password(form.password.data):
            return render_template("auth/login.html", form=form, error="invalid username or password")
        login_user(user)
        return redirect(url_for("index"))
    return render_template("auth/login.html", form=form)

@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).one_or_none()

@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for("auth_app.login"))

@auth_app.route("/login-as/", methods=["GET", "POST"], endpoint="login-as")
def login_as():
    if not (current_user.is_authenticated and current_user.is_staff):
        # non-admin users should not know about this feature
        raise NotFound

@auth_app.route("/logout/", endpoint="logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))

# @auth_app.route("/secret/")
# @login_required
# def secret_view():
#     return "Super secret data"

@auth_app.route("/register/", methods=["GET", "POST"], endpoint="register")
def register():
    if current_user.is_authenticated:
        return redirect("/")

    error = None
    form = RegistrationForm(request.form)
    if request.method == "POST" and form.validate_on_submit():
        if User.query.filter_by(username=form.username.data).count():
            form.username.errors.append("username already exists!")
            return render_template("auth/register.html", form=form)

        if User.query.filter_by(email=form.email.data).count():
            form.email.errors.append("email already exists!")
            return render_template("auth/register.html", form=form)

        user = User(
            fullname=form.fullname.data,
            username=form.username.data,
            email=form.email.data,
            is_staff=False,
        )
        # profile_pic = form.profile_pic.data
        # if profile_pic:
        #     filename = secure_filename(profile_pic.filename)
        #     profile_pic.save('./blog/images/' + filename)
        #     user.profile_pic = filename
        # user.profile_pic = form.profile_pic.data
        # avatar = user.profile_pic
        # if avatar:
        #     filename = secure_filename(avatar.filename)
        #     avatar.save('images/' + filename)
        #     user.profile_pic = filename
        # user.profile_pic = form.profile_pic.data
        # filename = secure_filename(user.profile_pic.filename)
        # pic_name = str(uuid.uuid1()) + "_" + filename
        # user.profile_pic.save(os.path.join(
        #     'images/'), pic_name)
        # user.profile_pic = pic_name
        user.password = form.password.data
        db.session.add(user)
        try:
            db.session.commit()
        except IntegrityError:
            current_app.logger.exception("Could not create user!")
            error = "Could not create user!"
        else:
            current_app.logger.info("Created user %s", user)
            login_user(user)
            return redirect(url_for("index"))
    return render_template("auth/register.html", form=form, error=error)

__all__ = [
    "login_manager",
    "auth_app",
]

