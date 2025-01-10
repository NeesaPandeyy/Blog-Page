from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,BooleanField
from wtforms.validators import DataRequired,Length,Email,EqualTo,ValidationError
from blogweb.models import User

class RegistrationForm(FlaskForm):
    """ A form for user registration.

    Attributes:
        username (StringField): This field requires characters between 2 and 20.
        email (StringField): This field requires a valid email address.
        password (PasswordField): The password box requires input.
        confirm_password (PasswordField):  This field must match the password field.
        submit (SubmitField): This button is used to register an account.
    """
    username = StringField('Username',validators=[DataRequired(),Length(min=2 , max=20)])
    email = StringField('Email',validators=[DataRequired(),Email()])
    password = PasswordField('Password',validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',validators=[DataRequired(),EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self,username):
        """ 
        Check for unique username 

        Args: 
            Takes username from the form

        Raises: 
            ValidationError if Username is already taken.

        """
        user = User.query.filter_by(username=username.data.lower()).first()
        if user:
            raise ValidationError('Username already taken')
        
    def validate_email(self,email):
        """ 
        Check for unique email address 

        Args: 
            Takes email address from the form

        Raises: 
            ValidationError if email address is already taken.

        """
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already taken')


class LoginForm(FlaskForm):
    """ A form for user login.

    Attributes:
        email (StringField): This field requires valid email address.
        password (PasswordField): The password box requires input.
        remember (BooleanField): A checkbox to remember the user for future logins.
        submit (SubmitField): The submit button to log in to the account.
    """
    email = StringField('Email',validators=[DataRequired(),Email()])
    password = PasswordField('Password',validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')