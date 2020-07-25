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
    def get_blog(cls):
        '''
        Function that returns all the data from blog after being queried
        '''
        blog = Post.query.order_by(Post.id.desc()).all()
        return blog

    @classmethod
    def delete_blog(cls):
        '''
        Functions the deletes a blog post
        '''
        blog = Blog.query.filter_by(id=blog_id).delete()
        comment = Comments.query.filter_by(blog_id=blog_id).delete()

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
    def get_comments(cls, post):
        comments = Comment.query.filter_by(post_id=post).all()
        return comments

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
