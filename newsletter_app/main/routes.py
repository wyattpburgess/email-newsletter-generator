from flask import render_template, Blueprint
from flask_login import login_required

main = Blueprint('main', __name__)


@main.route('/')
@login_required
def homepage():
    title = 'Welcome'
    return render_template('main/home.html', title=title, h1=title)
