from flask import Blueprint, render_template

errors = Blueprint('errors', __name__)


@errors.app_errorhandler(404)
def error_404(error):
    return render_template('errors/404.html', title='404 - Page Not Found', h1='Page Not Found (404)'), 404


@errors.app_errorhandler(403)
def error_403(error):
    return render_template('errors/403.html', title='403 - Permission Denied',
                           h1="You don't have permission to do that (403)"), 403


@errors.app_errorhandler(500)
def error_500(error):
    return render_template('errors/500.html', title='500 - Something Went Wrong', h1='Something went wrong (500)'), 500


