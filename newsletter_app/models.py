from datetime import datetime
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from newsletter_app import db, login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"


class Newsletter(db.Model):
    __tablename__ = 'newsletter'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    title = db.Column(db.String(100), nullable=False)
    intro = db.Column(db.Text)
    articles = db.relationship('Article', backref='article', lazy='dynamic', cascade="all,delete")

    def __repr__(self):
        return f"{self.title} -- {self.date.strftime('%B %m, %Y')} "


class Article(db.Model):
    __tablename__ = 'article'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    link = db.Column(db.String(400), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    content = db.Column(db.Text, nullable=False)
    newsletter_id = db.Column(db.Integer, db.ForeignKey('newsletter.id'), nullable=False)
    category = db.Column(db.Integer, db.ForeignKey('article_category.id'), nullable=False)
    category_name = db.relationship('ArticleCategory', foreign_keys=category)

    def __repr__(self):
        return f"Article('{self.title}', '{self.date}')"


class ArticleCategory(db.Model):
    __tablename__ = 'article_category'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f"{self.name}"
