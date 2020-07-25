from flask import render_template, request, redirect, url_for, abort,flash
from . import main
from ..models import User, Post
from .. import db
from .forms import UpdateProfile,PostForm,CommentForm
from flask_login import login_required, current_user
import datetime
from ..requests import get_quote


# Views


@main.route('/')
def index():
    '''
    View root page function that returns the index page and its data
    '''
    post=Post.get_blog()
    quote = get_quote()

    title = 'Home - Welcome to Perfect Blog app'



    return render_template('index.html', title=title,posts=post,quote=quote)


@main.route("/about")
def about():
    return render_template('about.html', title='About')

@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)
    return render_template("profile/profile.html", user = user)


@main.route('/user/<uname>/update', methods=['GET', 'POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username=uname).first()
    if user is None:
        abort(404)

    form = UpdateProfile()

    if form.validate_on_submit():
        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile', uname=user.username))

    return render_template('profile/update.html', form=form)


def new_post():
    post_form = PostForm()
    if post_form.validate_on_submit():
        title = post_form.title.data
        post = post_form.text.data
       

        # Updated pitch instance
        new_post = Post(post_title=title, post_content=post,
                          user=current_user, likes=0, dislikes=0)

        # Save pitch method
        new_post.save_post()
        return redirect(url_for('.index'))

    title = 'New pitch'
    return render_template('create_post.html', title=title, post_form=post_form)


@main.route('/post/<int:id>', methods=['GET', 'POST'])
def post(id):
    post = Post.get_post(id)
    posted_date = post.posted.strftime('%b %d, %Y')

    if request.args.get("like"):
        post.likes = post.likes + 1

        db.session.add(post)
        db.session.commit()

        return redirect("/post/{post_id}".format(post_id=post.id))

    elif request.args.get("dislike"):
        post.dislikes = post.dislikes + 1

        db.session.add(post)
        db.session.commit()

        return redirect("/post/{post_id}".format(post_id=post.id))

    comment_form = CommentForm()
    if comment_form.validate_on_submit():
        comment = comment_form.text.data

        new_comment = Comment(
            comment=comment, user=current_user, post_id=post)

        new_comment.save_comment()

    comments = Comment.get_comments(post)

    return render_template("post.html", post=post, comment_form=comment_form, comments=comments, date=posted_date)

    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)


@main.route("/post/<int:post_id>/update")
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Post has been updated!', 'success')
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post', form=form, legend='Update Post')



@main.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('main.index'))


@main.route('/blog/new/<int:id>', methods=['GET', 'POST'])
def new_comment(id):
    '''
    New comment function that returns a form to create a comment on a new page
    '''
    blogs = Post.query.filter_by(id=id).first()


    form = CommentForm()

    if form.validate_on_submit():
        comment_section = form.comment_section.data
        new_comment = Comments(
            comment_section=comment_section, blog_id=blogs.id)
        new_comment.save_comment()

        return redirect(url_for('.single_blog', id=blogs.id))

    title = 'New Comment'
    return render_template('new_comment.html', title=title, comment_form=form)
