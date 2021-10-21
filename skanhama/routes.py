from flask import render_template, url_for, flash, redirect
from skanhama import app
from skanhama.forms import RegistrationForm, LoginForm


@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html", title="Home")


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f"An email has been sent to the registered email for user {form.username.data}. Please "
              f"follow the activation link in the email to activate your account.", "success")
        return redirect(url_for("home"))
    return render_template("register.html", title="Register", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == "reddit@blog.com" and form.password.data == "reddit":
            flash("You have been successfully logged in.", "success")
            return redirect(url_for("home"))
        else:
            flash("Login unsuccessful. Please check username and password.", "fail")
    return render_template("login.html", title="Login", form=form)


@app.route("/browse")
def browse():
    return render_template("browse.html", title="Browse Packages")


@app.route("/upload")
def upload():
    return render_template("upload.html", title="Upload Package")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/faq")
def faq():
    return render_template("faq.html")
