from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileSize
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectField, MultipleFileField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from skanhama.models import User


class RegistrationForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=4, max=23)])
    email = StringField("Email", validators=[DataRequired(), Email(), Length(min=4, max=120)])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("Sign Up")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("That username is already taken. Please choose a different one.")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("An account with that email address already exists.")


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField("Remember Me")
    submit = SubmitField("Log In")


class ChangeUsername(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=4, max=23)])
    submit = SubmitField("Save")

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError("That username is already taken. Please choose a different one.")


class ChangeEmail(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email(), Length(min=4, max=120)])
    confirm_email = StringField("Confirm Email", validators=[DataRequired(),
                                                             Email(), Length(min=4, max=120), EqualTo("email")])
    submit = SubmitField("Save")

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError("That email is already in use. Please choose a different one.")


class UploadPackage(FlaskForm):
    # TODO: add base game as input
    name = StringField("Package Name", validators=[DataRequired()])
    version = StringField("Current Version", validators=[DataRequired(), Length(min=1, max=30)])
    author = StringField("Author(s) or Team", validators=[DataRequired()])
    summary = TextAreaField("Brief Description", validators=[DataRequired(), Length(min=1, max=230)])
    description = TextAreaField("Description", validators=[DataRequired(), Length(min=1, max=5000)])
    requirements = TextAreaField("Requirements", validators=[DataRequired()])
    category = SelectField("Primary Category", choices=["Combat", "Sex"], validators=[DataRequired()])
    game = SelectField("Game Version", choices=[(1, "Skyrim"), (2, "Skyrim Special Edition"),
                                                (3, "Skyrim Anniversary Edition")],
                       validators=[DataRequired()], default=2)
    nsfw = BooleanField("NSFW Content")
    package = FileField("Select Package", validators=[FileAllowed(["zip"]), FileSize(max_size=50*1024*1024)])
    banner = FileField("Select Banner Image", validators=[FileAllowed(["jpg", "gif", "png"]), FileSize(max_size=4*1024*1024)])
    gallery = MultipleFileField("Add Gallery Images", validators=[FileAllowed(["jpg", "gif", "png"]), FileSize(max_size=10*1024*1024)])
    upload = SubmitField("Upload")
