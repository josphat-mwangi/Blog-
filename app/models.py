from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_required,UserMixin
from datetime import datetime
from . import db, login_manager



class User(db.Model,UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    posts = db.relationship('Post', backref='author', lazy=True)
    pass_secure = db.Column(db.String(255))
    bio = db.Column(db.String(255))

    @property
    def password(self):
        raise AttributeError('You cannot read the password attribute')

    @password.setter
    def password(self, password):
        self.pass_secure = generate_password_hash(password)


    def verify_password(self, password):
        return check_password_hash(self.pass_secure, password)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

    
class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    category = db.Column(db.String)
    likes = db.Column(db.Integer)
    dislikes = db.Column(db.Integer)
    comments = db.relationship('Comment', backref='post_id', lazy="dynamic")



    def save_post(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_posts(cls):
        posts = Post.query.filter_by().all()
        return posts

    @classmethod
    def get_post(cls, id):
        post = Post.query.filter_by(id=id).first()

        return post

    @classmethod
    def count_posts(cls, uname):
        user = User.query.filter_by(username=uname).first()
        posts = Post.query.filter_by(user_id=user.id).all()

        posts_count = 0
        for post in posts:
            posts_count += 1

        return posts_count

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"


class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String(1000))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    post = db.Column(db.Integer, db.ForeignKey("posts.id"))

    def save_comment(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_comments(cls, pitch):
        comments = Comment.query.filter_by(post_id=post).all()
        return comments

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
