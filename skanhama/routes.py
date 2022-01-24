import secrets
import os.path
import sqlite3
import zipfile
import hashlib
import shutil
import json

from datetime import datetime
from pathlib import Path
from flask import render_template, url_for, flash, redirect, request, jsonify
from flask_login import login_user, current_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from skanhama import app, db
from skanhama.forms import RegistrationForm, LoginForm, ChangeUsername, ChangeEmail, UploadPackage
from skanhama.models import User, Package


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
    page = request.args.get("page", 1, type=int)
    packages = Package.query.order_by(Package.date_uploaded.desc()).paginate(page=page, per_page=25)
    return render_template("browse.html", title="Browse Packages", packages=packages)


# Processes the uploaded package
#
def process_package(form):
    processor_version = 0.1
    f_name, f_ext = os.path.splitext(form.package.data.filename)
    root_dir = Path(app.root_path, "static/packages", current_user.username)
    extracted_dir = Path(root_dir, str(form.name.data + "_" + form.version.data))
    package_dir = Path(extracted_dir)
    file_dict = {}

    # Check if dir already exists
    if Path(extracted_dir).exists():
        shutil.rmtree(extracted_dir)

    # Unzip zipfile to temporary directory and process
    # All .hkx files are consumed and stored in a .txt file in a JSON encoded
    # dictionary whereas all other files and the folder structure remains.
    # static\packages\[username]\[package]\[folder structure]\...
    # static\packages\[username]\[package]\animations_enc.txt
    with zipfile.ZipFile(form.package.data, "r") as zip_package:
        zip_package.extractall(extracted_dir)
        print(f"Zip file extracted: {extracted_dir}")
        paths = package_dir.glob("**/*.hkx")
        for path in paths:
            file_dict[hashlib.sha256(path.read_bytes()).hexdigest()] = [path.stat().st_size,
                                                                        str(path.relative_to(package_dir)),
                                                                        str(path.name)]
            path.unlink()
        # Write dictionary to database
        # for k, v in file_dict.items():

        json.dump(file_dict, open(Path(extracted_dir, "animations_enc.txt"), "w"))
        # for k, v in file_dict.items():
        #     anim = PackageAnimations(hash=k, size=v[0], relative_path=v[1], file_name=v[2])
        #     db.session.add(anim)
        # db.session.commit()
        #     print(f"Key: {k} | Value: {v}")

    # Return whether or not it was a valid package
    if file_dict:
        file_dict["_package_data"] = [processor_version, str(package_dir)]
    else:
        shutil.rmtree(extracted_dir)
    return file_dict


@app.route("/upload", methods=["GET", "POST"])
@login_required
def upload():
    print(app.root_path)
    form = UploadPackage()
    if form.validate_on_submit():
        if form.package.data:
            file_dict = process_package(form)
            if file_dict:
                print(f"package_data: {file_dict['_package_data'][1]}")
                pack = Package(name=form.name.data,
                               version=form.version.data,
                               author=current_user.username,
                               summary=form.summary.data,
                               description=form.description.data,
                               requirements=form.requirements.data,
                               package_dir=file_dict["_package_data"][1],
                               date_uploaded=datetime.now(),
                               downloads_total=0,
                               downloads_current_version=0,
                               views_total=0,
                               likes=0,
                               nsfw=form.nsfw.data,
                               user_id=current_user.id)
                db.session.add(pack)
                db.session.commit()
                flash("Your package was successfully uploaded.", "success")
            else:
                flash("Your package did not contain any .hkx files and has not been uploaded. Please ensure you "
                      "upload a package that contains valid Skyrim animation files.", "fail")
            return redirect(url_for("browse"))
    return render_template("upload.html", title="Upload Package", form=form)


@app.route("/package/<int:package_id>")
def package(package_id):
    pack = Package.query.get_or_404(package_id)
    return render_template("package.html", title=pack.name, pack=pack)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/faq")
def faq():
    return render_template("faq.html")


# @app.route("/livesearch", methods=["GET", "POST"])
# def livesearch():
#     # searchbox = request.form.get("text")
#     # con = sqlite3.connect("site.db")
#     # cursor = con.cursor()
#     # query = "select name from package where name LIKE '{}%' order by name".format(searchbox)
#     # cursor.execute(query)
#     # result = cursor.fetchall()
#     # return jsonify(result)
#     searchbox = request.form.get("text")
#     searchbox = '%' + searchbox + '%'
#     engine = create_engine('sqlite:///site.db', echo=True)
#     conn = engine.connect()
#     result = conn.engine.execute("select * from PACKAGE where name LIKE ? order by name LIMIT 4", searchbox).fetchall()
#     conn.close()
#     result= Convert(result)
#     return result
#
#
# def Convert(lst):
#     resultproxy = lst
#     d, a = {}, []
#     for rowproxy in resultproxy:
#         for column, value in rowproxy.items():
#             d = {**d, **{column: value}}
#         a.append(d)
#     return d
