from blog.app import app
from blog.models import User
from blog.models.database import db


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        debug=True,
    )


@app.cli.command("init-db")
def init_db():
    """
    Run in your terminal:
    flask init-db
    """
    db.create_all()
    print("done!")


@app.cli.command("create-users")
def create_users():
    """
    Run in your terminal:
    flask create-users
    > done! created users: <User #1 'admin'> <User #2 'james'>
    """

    admin1 = User(username="admin1", email="admin1@admin.com", is_staff=True)
    james1 = User(username="james1", email="james1@gmail.com")
    db.session.add(admin1)
    db.session.add(james1)
    db.session.commit()
    print("done! created users:", admin1, james1)