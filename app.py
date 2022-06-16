"""Blogly application."""

from crypt import methods
from flask import Flask, render_template, request, redirect
from models import db, connect_db, User, Post, Tag, PostTag

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()

@app.route('/')
def redirect_to_users():
    return redirect('/users')

@app.route('/users')
def list_users():
    '''Shows list of all users'''
    users = User.query.all()
    return render_template('base.html', users=users)

@app.route('/users/new')
def show_new_user_form():
    return render_template('new-user.html')

@app.route('/users/new', methods=["POST"])
def create_user():
    '''Create a new user'''
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    img_url = request.form["img_url"]

    new_user = User(first_name=first_name, last_name=last_name, img_url=img_url)
    db.session.add(new_user)
    db.session.commit()

    return redirect(f"/users/{new_user.id}")

@app.route('/users/<int:user_id>')
def show_user(user_id):
    '''Show details about a single user'''
    user = User.query.get_or_404(user_id)
    return render_template('details.html', user=user)

@app.route('/users/<int:user_id>')
def redirect_to_edit(user_id):
    return redirect(f'/users/{user_id}/edit')


@app.route('/users/<int:user_id>/edit')
def edit_user(user_id):
    user = User.query.get(user_id)
    return render_template('edit.html', user=user)

@app.route('/users/<int:user_id>/edit', methods=["POST"])
def submit_edit(user_id):
    
    user = User.query.get_or_404(user_id)

    user.first_name = request.form["first_name"]
    user.last_name = request.form["last_name"]
    user.img_url = request.form["img_url"]

    db.session.add(user)
    db.session.commit()

    return redirect(f'/users/{user.id}')

@app.route('/users/<int:user_id>/delete', methods=["POST"])
def delete_user(user_id):
    User.query.filter_by(id=user_id).delete()
    db.session.commit()

    return redirect("/users")

@app.route('/users/<int:user_id>/posts/new')
def show_new_post_form(user_id):
    tags = Tag.query.all()
    return render_template('new-post.html', tags=tags)

@app.route('/users/<int:user_id>/posts/new', methods=["POST"])
def add_new_post(user_id):
    user = User.query.get_or_404(user_id)
    tag_ids = [int(num) for num in request.form.getlist("tags")]
    tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

    user.title = request.form["title"]
    user.content = request.form["content"]
    user.id = user_id

    new_post = Post(title=user.title, content=user.content, user_id=user.id, tags=tags)

    db.session.add(new_post)
    db.session.commit()

    return redirect(f'/users/{user_id}')

@app.route('/posts/<int:post_id>')
def show_post(post_id):
    post = Post.query.get(post_id)
    user = User.query.get(post.user_id)
    return render_template('post.html', post=post, user=user)

@app.route('/posts/<int:post_id>/edit')
def edit_post_form(post_id):
    post = Post.query.get(post_id)
    tags = Tag.query.all()
    return render_template('edit-post.html', post=post, tags=tags)

@app.route('/posts/<int:post_id>/edit', methods=["POST"])
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    tag_ids = [int(num) for num in request.form.getlist("tags")]
    tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

    post.title = request.form["title"]
    post.content = request.form["content"]
    post.tags = tags

    db.session.add(post)
    db.session.commit()

    return redirect(f'/posts/{post_id}')

@app.route('/posts/<int:post_id>/delete', methods=["POST"])
def delete_post(post_id):
    Post.query.filter_by(id=post_id).delete()
    db.session.commit()

    return redirect('/users')

@app.route('/tags')
def list_tags():
    tags = Tag.query.all()
    return render_template('tags.html', tags=tags)

@app.route('/tags/<int:tag_id>')
def tag_info(tag_id):
    tag = Tag.query.get(tag_id)
    posts = tag.posts
    return render_template('tag-details.html', tag=tag, posts=posts)

@app.route('/tags/new')
def new_tag_form():
    return render_template('new-tag.html')

@app.route('/tags/new', methods=["POST"])
def add_new_tag():
    name = request.form["name"]

    new_tag = Tag(name=name)
    db.session.add(new_tag)
    db.session.commit()

    return redirect('/tags')

@app.route('/tags/<int:tag_id>/edit')
def edit_tag_form(tag_id):
    tag = Tag.query.get(tag_id)

    return render_template('edit-tag.html', tag=tag)

@app.route('/tags/<int:tag_id>/edit', methods=["POST"])
def edit_tag(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    name = request.form["name"]

    tag.name = name
    db.session.add(tag)
    db.session.commit()

    return redirect('/tags')

@app.route('/tags/<int:tag_id>/delete', methods=["POST"])
def delete_tag(tag_id):
    PostTag.query.filter_by(tag_id=tag_id).delete()

    Tag.query.filter_by(id=tag_id).delete()
    db.session.commit()

    return redirect('/tags')





