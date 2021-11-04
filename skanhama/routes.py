import os.path, zipfile
import secrets
from pathlib import Path
from datetime import datetime
from flask import render_template, url_for, flash, redirect, request
from flask_login import login_user, current_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from skanhama import app, db
from skanhama.models import User
from skanhama.forms import RegistrationForm, LoginForm, ChangeUsername, ChangeEmail, UploadPackage


@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html", title="Home")


@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, "sha256")
        user = User(username=form.username.data, email=form.email.data, password=hashed_password,
                    registered_on=datetime.now(), confirmed=False, admin=False)
        db.session.add(user)
        db.session.commit()
        flash(f"An email has been sent to the registered email for user {form.username.data}. Please "
              f"follow the activation link in the email to activate your account.", "success")
        return redirect(url_for("home"))
    return render_template("register.html", title="Register", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get("next")
            return redirect(next_page) if next_page else redirect(url_for("home"))
        else:
            flash("Log in unsuccessful. Please check email and password.", "fail")
    return render_template("login.html", title="Log In", form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))


@app.route("/account/overview", methods=["GET", "POST"])
@login_required
def account():
    return render_template("account/overview.html", title="Account Overview")


@app.route("/account/username", methods=["GET", "POST"])
@login_required
def account_username():
    form = ChangeUsername()
    if form.validate_on_submit():
        if current_user.username == form.username.data:
            flash("Cannot change account username to the one you currently have.", "fail")
        else:
            current_user.username = form.username.data
            db.session.commit()
            flash("Your account username has been successfully changed.", "success")
            return redirect(url_for("account"))
    elif request.method == "GET":
        form.username.data = current_user.username
    return render_template("account/username.html", title="Change Username", form=form)


@app.route("/account/email", methods=["GET", "POST"])
@login_required
def account_email():
    form = ChangeEmail()
    if form.validate_on_submit():
        if current_user.email == form.email.data:
            flash("Cannot change account email to the one you currently have.", "fail")
        else:
            current_user.email = form.email.data
            db.session.commit()
            flash("Your account email has been successfully changed.", "success")
            return redirect(url_for("account"))
    elif request.method == "GET":
        form.email.data = current_user.email
    return render_template("account/email.html", title="Change Email", form=form)


@app.route("/account/password")
@login_required
def account_password():
    return render_template("account/password.html", title="Change Email")


@app.route("/account/data")
@login_required
def account_data():
    return render_template("account/data.html", title="Personal Data")


@app.route("/browse")
def browse():
    return render_template("browse.html", title="Browse Packages")


def process_package(form_package):
    with zipfile.ZipFile(form_package, "r") as zip_package:
        temp_dir = secrets.token_hex(8)
        p_path = os.path.join(app.root_path, "static/package_temp", temp_dir)
        zip_package.extractall(p_path)
        print(f"Zip file extracted to temp_dir: {p_path}")
        paths = Path(p_path).glob("**/*.hkx")
        for path in paths:
            print("-------------------------------------------------------------------------------------------------------------")
            print(str(path))
            print(f"{str(path.name)} - {path.stat().st_size / 1024}kb")

        return 1
        # for file in os.listdir(os.fsencode(p_path)):
        #     if file.endswith(".hkx"):
        #         print(file)
        #     return 1
        # else:
        #     print("No .hkx files found in the uploaded package.")
        #     return 0


@app.route("/upload", methods=["GET", "POST"])
@login_required
def upload():
    print(app.root_path)
    form = UploadPackage()
    if form.validate_on_submit():
        if form.package.data:
            if process_package(form.package.data) == 0:
                flash("Your package did not contain any .hkx files and has not been uploaded. Please ensure you"
                      "upload a package that contains valid Skyrim animation files.", "fail")
            else:
                flash("Your package has been successfully uploaded.", "success")
        return redirect(url_for("browse"))
    return render_template("upload.html", title="Upload Package", form=form)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/faq")
def faq():
    return render_template("faq.html")
