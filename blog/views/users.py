from flask import Blueprint, render_template, abort
from werkzeug.exceptions import NotFound
from blog.models import User, Author, Article

users_app = Blueprint("users_app", __name__)

@users_app.route("/<int:user_id>/", endpoint="details")
def user_details(user_id: int):
    user = User.query.filter_by(id=user_id).one_or_none()
    if user is None:
        raise NotFound(f"User #{user_id} doesn't exist!")
    return render_template("users/details.html", user=user)

@users_app.route("/my_profile/<int:user_id>/", endpoint="profile")
def user_profile(user_id: int):
    user = User.query.filter_by(id=user_id)
    if user:
        return render_template('users/profile.html', user=user)
    else:
        return 'User not found'

@users_app.route('/<int:author_id>/articles/', endpoint="user_articles")
def show_author_articles(author_id):
    author = Author.query.get(author_id)
    if author is None:
        abort(404)
    articles = Article.query.filter_by(author_id=author_id).all()
    return render_template('articles/user_articles.html', author=author, articles=articles)

@users_app.route("/", endpoint='list')
def users_list():
    users = User.query.all()
    return render_template("users/list.html", users=users)