from flask import render_template,url_for,request,Blueprint
from blogweb.models import User,Post
from flask_login import current_user,login_required

main = Blueprint('main',__name__)

@main.route("/")
@main.route("/home")
@login_required
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=3)
    return render_template('home.html', posts=posts)


@main.route("/account")
@main.route("/account/<username>")
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

