"""Blogly application."""

from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post, Tag, PostTag

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "blogly"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['DEBUG'] = True
debug = DebugToolbarExtension(app)

connect_db(app)
with app.app_context():
    
    db.create_all()

@app.route('/')
def root():
    """Homepage show top 5 post by time created"""

    posts = Post.query.order_by(Post.created_at.desc()).limit(5).all()
    return render_template("posts/homepage.html", posts=posts)

@app.errorhandler(404)
def page_not_found(e):
    """Show 404 NOT FOUND page"""

    return render_template('404.html'), 404
####################################################################################
# USERS ROUTE

@app.route('/users')
def users_index():
    """Shows list of users"""
    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template('users/index.html', users=users)

@app.route('/users/new', methods=["GET"])
def users_new_form():
    """Registers with new user form"""
    return render_template("users/new.html")

@app.route("/users/new", methods=["POST"])
def users_new():
    """Handle form submission for creating a new user"""

    new_user = User(
        first_name=request.form['first_name'],
        last_name= request.form['last_name'],
        image_url=request.form['image_url'] or None
    )
    db.session.add(new_user)
    db.session.commit()

    return redirect("/users")


@app.route('/users/<int:user_id>')
def user_show(user_id):
    """Show a page with info on a specific user"""

    user = User.query.get_or_404(user_id)
    return render_template('users/show.html', user=user)

@app.route('/users/<int:user_id>/edit')
def user_edit(user_id):
    """Show a form to edit an exsiting user."""
    
    user = User.query.get_or_404(user_id)
    return render_template('users/edit.html', user=user)

@app.route('/users/<int:user_id>/edit', methods=["POST"])
def users_update(user_id):
    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first_name'],
    user.last_name= request.form['last_name'],
    user.image_url=request.form['image_url']

    db.session.add(user)
    db.session.commit()
    return redirect("/users")

@app.route('/users/<int:user_id>/delete', methods=["POST"])
def user_destroy(user_id):
    
    user =User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash(f"User {user.full_name} deleted.")

    return redirect("/users")
# #############################################################################
# POST ROUTES

@app.route("/users/<int:user_id>/posts/new", methods=["GET"])
def new_post_form(user_id):
    """User form to submit new post"""
    user = User.query.get_or_404(user_id)
    return render_template('posts/new.html', user=user)

@app.route("/users/<int:user_id>/posts/new", methods=["POST"])
def posts_new(user_id):
    """Handle form submission for creating a new post for a specific user"""
    user = User.query.get_or_404(user_id)
    new_post = Post(title=request.form['title'],
                    content=request.form['content'],
                     user=user)
    
    db.session.add(new_post)
    db.session.commit()
    flash(f"Post '{new_post.title}' added.")

    return redirect(f"/users/{user_id}")

@app.route("/posts/<int:post_id>")
def posts_show(post_id):
    """Show a page with info on a specific post"""

    post= Post.query.get_or_404(post_id)
    return render_template("posts/show.html", post=post)

@app.route('/posts/<int:post_id>/edit')
def post_edit(post_id):
    """Show a form to edit an existing post"""

    post = Post.query.get_or_404(post_id)

    return render_template('posts/edit.html', post=post)

@app.route('/posts/<int:post_id>/edit', methods=["POST"])
def post_update(post_id):
    """Handle form submission for updating an existing post"""

    post = Post.query.get_or_404(post_id)
    post.title = request.form['title']
    post.content= request.form['content']

    db.session.add(post)
    db.session.commit()
    return redirect(f"/users/{post.user_id}")

@app.route('/posts/<int:post_id>/delete', methods=["POST"])
def posts_destroy(post_id):
    
    post =Post.query.get_or_404(post_id)

    db.session.delete(post)
    db.session.commit()
    flash(f"Post {post.title} is deleted.")

    return redirect(f"/users/{post.user_id}")
# ######################################################################################
# Tag Routes
@app.route('/tags')
def tag_index():
    """Show a page with info on all tags"""

    tags = Tag.query.all()

    return render_template('tags/index.html', tags=tags)

@app.route('/tags/new')
def new_tag_form():
    """Show a form to create a new tag"""

    posts = Post.query.all()

    return render_template('tags/new.html', posts=posts)

@app.route('/tags/new', methods=["POST"])
def tags_new():
    """Handle form submission for creating a new tag"""
    post_ids = [int(num) for num in request.form.getlist("posts")]
    posts = Post.query.filter(Post.id.in_(post_ids)).all()
    new_tag = Tag(name=request.form['name'], posts=posts)

    db.session.add(new_tag)
    db.session.commit()
    flash(f"Tag '{new_tag.name}' added.")

    return redirect("/tags")

@app.route('/tags/<int:tag_id>')
def tags_show(tag_id):
    """Show a page with info on a specific tag"""

    tag = Tag.query.get_or_404(tag_id)
    return render_template('tags/show.html', tag=tag)

@app.route('/tags/<int:tag_id>/edit')
def tags_edit_form(tag_id):
    """Show a form to edit an existing tag"""

    tag = Tag.query.get_or_404(tag_id)
    posts = Post.query.all()
    return render_template('tags/edit.html', tag=tag, posts=posts)


@app.route('/tags/<int:tag_id>/edit', methods=["POST"])
def tags_edit(tag_id):
    """Handle form submission for updating an existing tag"""

    tag = Tag.query.get_or_404(tag_id)
    tag.name = request.form['name']
    post_ids = [int(num) for num in request.form.getlist("posts")]
    tag.posts = Post.query.filter(Post.id.in_(post_ids)).all()

    db.session.add(tag)
    db.session.commit()
    flash(f"Tag '{tag.name}' edited.")

    return redirect("/tags")

@app.route('/tags/<int:tag_id>/delete', methods=["POST"])
def tags_destroy(tag_id):
    """Handle form submission for deleting an existing tag"""

    tag = Tag.query.get_or_404(tag_id)
    db.session.delete(tag)
    db.session.commit()
    flash(f"Tag '{tag.name}' deleted.")

    return redirect("/tags")