from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,TextAreaField
from wtforms.validators import DataRequired

class PostForm(FlaskForm):
    """ A form to post blogs.

    Attributes:
        title (StringField): A required text area for user to write title of content.
        content (TextAreaField): A required text area for user to write content.
        submit (SubmitField): The submit button used to publish the post.
    """

    title = StringField('Title',validators=[DataRequired()])
    content = TextAreaField('Content',validators=[DataRequired()])
    submit = SubmitField('Post')
