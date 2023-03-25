from flask_wtf import FlaskForm
from wtforms import StringField, validators, PasswordField, SubmitField
from flask_wtf.file import FileField, FileAllowed
class UserBaseForm(FlaskForm):
    fullname = StringField("Fullname")
    username = StringField(
        "username",
        [validators.DataRequired()],
    )
    email = StringField(
        "Email Address",
        [
            validators.DataRequired(),
            validators.Email(),
            validators.Length(min=6, max=200),
        ],
        filters=[lambda data: data and data.lower()],
    )
class RegistrationForm(UserBaseForm):
    password = PasswordField(
        "New Password",
        [
            validators.DataRequired(),
            validators.EqualTo("confirm", message="Passwords must match"),
        ],
    )
    # profile_pic = FileField("Avatar", validators=[
    #                         FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')])
    confirm = PasswordField("Repeat Password")
    submit = SubmitField("Register")
class LoginForm(FlaskForm):
    username = StringField(
        "username",
        [validators.DataRequired()],
    )
    password = PasswordField(
        "Password",
        [validators.DataRequired()],
    )
    submit = SubmitField("Login")