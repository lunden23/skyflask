from datetime import datetime
from skanhama import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False)
    confirmed = db.Column(db.Boolean, nullable=False, default=False)
    confirmed_on = db.Column(db.DateTime, nullable=True)
    uploads = db.relationship("Package", backref="upload_author", lazy="dynamic")
    comments = db.relationship("Comment", backref="comment_author", lazy="dynamic")

    def __repr__(self):
        return f"User ('{self.id}', '{self.username}', '{self.email}', '{self.confirmed_on}, 'Admin={self.admin}')"


class Package(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, index=True, nullable=False)
    version = db.Column(db.String(30), nullable=False)
    author = db.Column(db.String(100), index=True, nullable=False)
    nsfw = db.Column(db.Boolean, nullable=False)
    summary = db.Column(db.String(230), nullable=False)
    description = db.Column(db.Text, nullable=False)
    requirements = db.Column(db.Text, nullable=False)
    package_dir = db.Column(db.String(400), nullable=False, unique=True)
    date_uploaded = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    downloads_total = db.Column(db.BigInteger, index=True, nullable=False)
    downloads_current_version = db.Column(db.BigInteger, nullable=False)
    likes = db.Column(db.BigInteger, index=True, nullable=False)
    views_total = db.Column(db.BigInteger, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    category = db.relationship("Categories", backref="category_id", lazy=True)
    comments = db.relationship("Comment", backref="package_comments", lazy=True)
    games = db.relationship("Games", backref="games_id", lazy=True)

    def __repr__(self):
        return f"Package ('{self.date_uploaded}', {self.id}', '{self.name}', '{self.uploaderl}', '{self.synposis}')"


class PackageAnimations(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    version = db.Column(db.String, nullable=False, unique=True)
    package_id = db.Column(db.Integer, db.ForeignKey("package.id"), nullable=False)

    def __repr__(self):
        return f"Animation file: {self.hash} | {self.size}, {self.relative_path}, {self.file_name}"


class Categories(db.Model):
    id = db.Column(db.Integer, db.ForeignKey("package.id"), primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)

    def __repr__(self):
        return f"Package ('{self.id}', {self.name}')"


class Games(db.Model):
    id = db.Column(db.Integer, db.ForeignKey("package.id"), primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    package = db.Column(db.Integer, db.ForeignKey("package.id"), nullable=False)
