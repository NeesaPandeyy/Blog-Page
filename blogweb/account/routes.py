from flask import render_template,url_for,flash,redirect,request,Blueprint
from blogweb import  db, bcrypt
from blogweb.account.forms import RegistrationForm,LoginForm
from blogweb.models import User
from flask_login import login_user,logout_user,current_user


account = Blueprint('account',__name__)

@account.route("/register",methods = ['POST','GET'])
def register():
    """
    Handles user registration process.

    If the given data are valid then it creates user,create and save hashed password
    in database.Also flashes a success message.
    
    """
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username= form.username.data.lower(),email=form.email.data,password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Account created successfully!!','success')
        return redirect(url_for('account.login'))
    return render_template('register.html', title='Register',form = form)

@account.route("/login", methods=['GET', 'POST'])
def login():
    """
    Handles user login process.

    If the given data are valid then users are directed to home page and 
    flashes a success message.But if data are not valid it flashes a unsuccessful
    message.
    
    """
    form = LoginForm()
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    if form.validate_on_submit():
        user=User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user , remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Login Unsuccessful.Check your email and password','danger')
    return render_template('login.html',title='Login',form=form)


@account.route("/logout")
def logout():
    """
    Logout the user and redirect them to login page.
    """
    logout_user()
    return redirect(url_for('account.login'))
