from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_required
from newsletter_app import db
from newsletter_app.models import Newsletter, Article, ArticleCategory
from newsletter_app.newsletter.forms import NewsletterForm, CategoryForm, ArticleForm, DeletePostForm, \
    SendNewsletterForm
from newsletter_app.newsletter.utils import send_newsletter_email

newsletter = Blueprint('newsletter', __name__)


@newsletter.route('/create-newsletter', methods=['GET', 'POST'])
@login_required
def new_newsletter():
    form = NewsletterForm()
    if form.validate_on_submit():
        newsletter = Newsletter(title=form.title.data, intro=form.intro.data, date=form.date.data)
        db.session.add(newsletter)
        db.session.commit()
        flash(f'The newsletter "{form.title.data}" has been created for the date '
              f'{form.date.data}', 'alert-success')
        return redirect(url_for('newsletter.update_newsletter', newsletter_id=newsletter.id))
    title = 'Create a Newsletter'
    return render_template('newsletter/create_newsletter.html', title=title, h1=title, form=form)


@newsletter.route("/newsletter/<int:newsletter_id>/add-article", methods=['GET', 'POST'])
@login_required
def article(newsletter_id):
    form = ArticleForm()
    if form.validate_on_submit():
        article = Article(category=form.category.data.id, title=form.title.data, link=form.link.data,
                          date=form.date.data, content=form.content.data, newsletter_id=newsletter_id)
        db.session.add(article)
        db.session.commit()
        flash(f'The article "{form.title.data}" has been added to the newsletter.', 'alert-success')
        return redirect(url_for('newsletter.update_newsletter', newsletter_id=newsletter_id))
    title = 'Add an Article'
    return render_template('newsletter/article.html', title=title, h1=title, form=form, newsletter_id=newsletter_id)


@newsletter.route('/manage')
@login_required
def manage():
    title = 'Manage Newsletters'
    newsletters = Newsletter.query.all()
    return render_template('newsletter/manage_newsletter.html', title=title, h1=title, newsletters=newsletters)


@newsletter.route("/newsletter/<int:newsletter_id>/update", methods=['GET', 'POST'])
@login_required
def update_newsletter(newsletter_id):
    newsletter = Newsletter.query.get_or_404(newsletter_id)
    form = NewsletterForm()
    if form.validate_on_submit():
        if form.submit.data:
            newsletter.date = form.date.data
            newsletter.title = form.title.data
            newsletter.intro = form.intro.data
            db.session.commit()
            flash('Your newsletter has been updated!', 'alert-success')
            return redirect(url_for('newsletter.update_newsletter', newsletter_id=newsletter.id))
    elif request.method == 'GET':
        form.date.data = newsletter.date
        form.title.data = newsletter.title
        form.intro.data = newsletter.intro
    title = 'Update Newsletter'
    articles = Article.query.filter(Article.newsletter_id == newsletter_id)
    return render_template('newsletter/edit_newsletter.html', title=title, h1=title,
                           form=form, articles=articles, newsletter_id=newsletter_id)


@newsletter.route("/newsletter/<int:newsletter_id>/delete", methods=['GET', 'POST'])
@login_required
def delete_newsletter(newsletter_id):
    form = DeletePostForm()
    if form.validate_on_submit():
        if form.submit.data:
            newsletter = Newsletter.query.get_or_404(newsletter_id)
            db.session.delete(newsletter)
            db.session.commit()
            flash('Your newsletter has been deleted!', 'alert-success')
        # redirect if form is submitted or if cancelled
        return redirect(url_for('newsletter.manage'))
    title = "Delete Newsletter"
    return render_template('newsletter/delete.html', title=title, h1=title, form=form, type='newsletter')


@newsletter.route("/article/<int:article_id>/update", methods=['GET', 'POST'])
@login_required
def update_article(article_id):
    article = Article.query.get_or_404(article_id)
    newsletter_id = Article.query.filter(Article.id == article_id).first().newsletter_id
    form = ArticleForm()
    if form.validate_on_submit():
        if form.submit.data:
            article.category = form.category.data.id
            article.title = form.title.data
            article.link = form.link.data
            article.date = form.date.data
            article.content = form.content.data
            db.session.commit()
            flash('Your article has been updated!', 'alert-success')
            return redirect(url_for('newsletter.update_newsletter', newsletter_id=newsletter_id))
    elif request.method == 'GET':
        category = ArticleCategory.query.filter_by(id=article.category).first()
        form.category.data = category
        form.title.data = article.title
        form.link.data = article.link
        form.date.data = article.date
        form.content.data = article.content
    title = 'Update Article'
    return render_template('newsletter/article.html', title=title, h1=title,
                           form=form, article_id=article_id)


@newsletter.route("/article/<int:article_id>/delete", methods=['GET', 'POST'])
@login_required
def delete_article(article_id):
    form = DeletePostForm()
    newsletter_id = Article.query.filter(Article.id == article_id).first().newsletter_id
    if form.validate_on_submit():
        # if submit button is clicked
        if form.submit.data:
            article = Article.query.get_or_404(article_id)
            db.session.delete(article)
            db.session.commit()
            flash('Your article has been deleted!', 'alert-success')
        # redirect if form is submitted or if cancelled
        return redirect(url_for('newsletter.update_newsletter', newsletter_id=newsletter_id))
    title = "Delete Article"
    return render_template('newsletter/delete.html', title=title, h1=title, form=form, type='article')


@newsletter.route("/preview/<int:newsletter_id>", methods=['GET', 'POST'])
@login_required
def preview(newsletter_id):
    newsletter = Newsletter.query.get_or_404(newsletter_id)
    articles = Article.query.filter(Article.newsletter_id == newsletter_id)
    form = SendNewsletterForm()
    if form.validate_on_submit():
        if form.submit.data:
            # creates list of strings split on commas
            to = form.to.data.split(',')
            cc = form.cc.data.split(',')
            bcc = form.bcc.data.split(',')
            subject = form.subject.data
            try:
                send_newsletter_email(newsletter=newsletter, articles=articles, subject=subject, to=to, cc=cc, bcc=bcc)
                flash('The newsletter has been sent!', 'alert-success')
            except:
                flash('The newsletter failed to send. Please double check your inputs before '
                      'trying again.', 'alert-danger')
        return redirect(url_for('newsletter.preview', newsletter_id=newsletter_id))
    return render_template('newsletter/preview.html', title='Preview', form=form, articles=articles, newsletter=newsletter)


@newsletter.route("/manage-categories", methods=['GET', 'POST'])
@login_required
def manage_categories():
    title = 'Manage Newsletter Section Headings'
    categories = ArticleCategory.query.all()
    return render_template('newsletter/manage_category.html', title=title, h1=title, categories=categories)


@newsletter.route('/newsletter/categories/add-category', methods=['GET', 'POST'])
@login_required
def add_category():
    form = CategoryForm()
    if form.validate_on_submit():
        category = ArticleCategory(name=form.name.data)
        db.session.add(category)
        db.session.commit()
        flash(f'The category "{form.name.data}" has been created,', 'alert-success')
        return redirect(url_for('newsletter.manage_categories'))
    title = "Newsletter Section"
    return render_template('newsletter/edit_category.html', title=title, h1=title, h2='Add Section Heading', form=form)


@newsletter.route("/newsletter/categories/<int:category_id>/update", methods=['GET', 'POST'])
@login_required
def update_category(category_id):
    category = ArticleCategory.query.get_or_404(category_id)
    form = CategoryForm()
    if form.validate_on_submit():
        if form.submit.data:
            category.name = form.name.data
            db.session.commit()
            flash('Your newsletter section has been updated!', 'alert-success')
            return redirect(url_for('newsletter.manage_categories'))
    elif request.method == 'GET':
        form.name.data = category.name
    title = 'Update Newsletter Section Heading'
    return render_template('newsletter/edit_category.html', title=title, h1=title, h2='Manage Section Heading', form=form)


@newsletter.route("/newsletter/categories/<int:category_id>/delete", methods=['GET', 'POST'])
@login_required
def delete_category(category_id):
    form = DeletePostForm()
    if form.validate_on_submit():
        # if submit button is clicked
        if form.submit.data:
            category = ArticleCategory.query.get_or_404(category_id)
            db.session.delete(category)
            db.session.commit()
            flash('Your newsletter section has been deleted!', 'alert-success')
        # redirect if form is submitted or if cancelled
        return redirect(url_for('newsletter.manage_categories'))
    title = "Delete Newsletter Section Heading"
    return render_template('newsletter/delete.html', title=title, h1=title, form=form, type='newsletter section heading')
