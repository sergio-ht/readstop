from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from app import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default="default.jpg")
    password = db.Column(db.String(60), nullable=False)
    reviews = db.relationship("Review", backref="author", lazy=True)

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config["SECRET_KEY"], expires_sec)
        return s.dumps({"user_id": self.id}).decode("utf-8")

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config["SECRET_KEY"])
        try:
            user_id = s.loads(token)["user_id"]
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self) -> str:
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    article_id = db.Column(db.Integer, db.ForeignKey("article.id"), nullable=False)

    def __repr__(self) -> str:
        return f"Post('{self.rating}', '{self.date_posted}')"


ArticleTag = db.Table(
    "ArticleTag",
    db.Column("article_id", db.Integer, db.ForeignKey("article.id"), primary_key=True),
    db.Column("tag_id", db.Integer, db.ForeignKey("tag.id"), primary_key=True),
)


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(120), unique=True, nullable=False)
    title = db.Column(db.String(120), nullable=False, default="No title available")
    image_file = db.Column(db.String(20), nullable=False, default="default.jpg")
    reviews = db.relationship("Review", backref="article", lazy=True)
    tags = db.relationship(
        "Tag", secondary=ArticleTag, backref=db.backref("articles", lazy=True)
    )

    def __repr__(self) -> str:
        return f"Article('{self.title}', '{self.url}')"


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)

    def __repr__(self) -> str:
        return f"Tag('{self.name}')"
