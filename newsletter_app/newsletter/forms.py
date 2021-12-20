from flask_wtf import FlaskForm
from wtforms.fields.html5 import DateField, URLField
from wtforms.fields import StringField, SubmitField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired, URL, Optional
from wtforms.widgets import TextArea
from newsletter_app.models import ArticleCategory


class ArticleForm(FlaskForm):
    title = StringField('Article Title', validators=[DataRequired()])
    link = URLField('Article Link', validators=[DataRequired(), URL(message='Please enter a valid URL')])
    date = DateField('Date Published', format='%Y-%m-%d', validators=[DataRequired()])
    content = StringField('Article Summary', widget=TextArea(), validators=[DataRequired()])
    category = QuerySelectField('Category', validators=[DataRequired()],
                                query_factory=lambda: ArticleCategory.query.all())
    submit = SubmitField("Submit")


class NewsletterForm(FlaskForm):
    date = DateField('Newsletter Date', format='%Y-%m-%d', validators=[DataRequired()])
    title = StringField('Newsletter Title', validators=[DataRequired()])
    intro = StringField('Introduction', widget=TextArea(), validators=[DataRequired()])
    submit = SubmitField('Submit')


class DeletePostForm(FlaskForm):
    submit = SubmitField('Delete')
    cancel = SubmitField('Cancel')


class CategoryForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    submit = SubmitField('Add Category')


class SendNewsletterForm(FlaskForm):
    to = StringField('To', validators=[DataRequired()])
    cc = StringField('CC', validators=[Optional()])
    bcc = StringField('BCC', validators=[Optional()])
    subject = StringField('Email Subject', validators=[Optional()])
    submit = SubmitField('Send Newsletter')
