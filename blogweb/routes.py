from flask import render_template,url_for,flash,redirect,request,abort
from blogweb import app, db, bcrypt
from blogweb.forms import RegistrationForm,LoginForm,PostForm
from blogweb.models import User,Post
from flask_login import login_user,logout_user,current_user,login_required

@app.route("/")
@app.route("/home")
@login_required
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=3)
    return render_template('home.html', posts=posts)

@app.route("/register",methods = ['POST','GET'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username= form.username.data,email=form.email.data,password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Account created successfully!!','success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register',form = form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    if form.validate_on_submit():
        user=User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user , remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful.Check your email and password','danger')
    return render_template('login.html',title='Login',form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/account")
@app.route("/account/<username>")
@login_required
def account(username=None):
    profile = url_for('static', filename='profilefile/' + current_user.profile)

    if username:
        page = request.args.get('page', 1, type=int)
        user = User.query.filter_by(username=username).first_or_404()
        posts = Post.query.filter_by(author=user)\
            .order_by(Post.date_posted.desc())\
            .paginate(page=page, per_page=3)
        has_posts = len(posts.items) > 0
        return render_template('account.html', title=f"{user.username}'s Posts", profile=profile, posts=posts, user=user,has_posts=has_posts)
    else:
        profile = url_for('static', filename='profilefile/' + current_user.profile)
        posts = Post.query.filter_by(author=current_user)\
            .order_by(Post.date_posted.desc())\
            .paginate(page=request.args.get('page', 1, type=int), per_page=3)
        has_posts = len(posts.items) > 0
        return render_template('account.html', title='Account', profile=profile, posts=posts, user=current_user, has_posts=has_posts)

@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def create_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data,content=form.content.data,author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Created','success')
        return redirect(url_for('home'))
    return render_template('createpost.html',title = 'NewPost',form = form,legend= 'New Post')

@app.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html',title = post.title ,post =post)

@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
def updatepost(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Successfully updated!!','success')
        return redirect(url_for('post',post_id=post_id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('createpost.html',title = 'Update Post' ,form =form,legend= 'Update Post')

@app.route("/post/<int:post_id>/delete", methods=['POST'])
def deletepost(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Successfully deleted!', 'success')
    return redirect(url_for('home'))
