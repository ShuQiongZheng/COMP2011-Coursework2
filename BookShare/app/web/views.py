from flask import render_template, redirect, url_for, request, flash, session, make_response, abort
from flask.json import jsonify
from flask_login import current_user, login_required, logout_user, login_user
from werkzeug.security import generate_password_hash
from app.models import *
from app.web.forms import BookForm, RegistrationForm, LoginForm
from app import db, login_manager, app
from . import web_bp


@web_bp.route('/', methods=['GET', 'POST'])
@login_required
def Show_book_list():
    form = BookForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            # Create a piece of data and submit the database using add
            db.session.add(Book(current_user.id, form.title.data, form.description.data, form.author.data))
            db.session.commit()
            flash('You have add a new book', 'success')
            return redirect(url_for('web.Show_book_list'))
        else:
            # When the form is invalid, an error message is displayed
            flash(form.errors, 'error')
            app.logger.info('%s failed to Show_book_list', current_user.username)
            abort(401)


    pagination = Book.query.filter_by().paginate(page=int(request.args.get('page', 1)),per_page=6)
    booklists = pagination.items

    return render_template('index.html', paginate=pagination, booklists=booklists, form=form)

@web_bp.route('/my_book/', methods=['GET', 'POST'])
@login_required
def my_book():
    form = BookForm()
    # add a new book
    if request.method == 'POST':
        if form.validate_on_submit():
            booklist = Book(current_user.id, form.title.data, form.description.data, form.author.data)
            if form.algorithms.data == True:
                booklist.tag.append(Tag.query.get(1))
            if form.programming.data == True:
                booklist.tag.append(Tag.query.get(2))
            if form.math.data == True:
                booklist.tag.append(Tag.query.get(3))
            if form.software.data == True:
                booklist.tag.append(Tag.query.get(4))
            if form.other.data == True:
                booklist.tag.append(Tag.query.get(5))

            db.session.add(booklist)
            db.session.commit()

            flash('You have add a new book', 'success')
            return redirect(url_for('web.my_book'))
        else:
            flash('Be caution: The author and title characters '
            'should not be more than 25 characters, and the description segment should not be more than 1,000 characters ', 'error')
            app.logger.info('%s failed to add one book', current_user.username)

            return redirect(url_for('web.my_book'))

    elif request.method == 'GET':
        page = int(request.args.get('page', 1))
        pagination = Book.query.filter_by(user_id=current_user.id).paginate(page=page, per_page=6)
        booklist = pagination.items
        return render_template('own_book.html', paginate=pagination, booklist=booklist, form=form)


@web_bp.route('/show_book/<int:id>/', methods=['GET', 'POST'])
@login_required
def show_book(id):
    form = Book.query.filter_by(id=id).first_or_404()

    string = ""
    for tag in form.tag:
           string += tag.name

    return render_template('show_book.html', form=form, string=string)

@web_bp.route('/like/<int:id>/', methods=['GET', 'POST'])#函数功能：点赞，返回原页面
@login_required
def like(id):
    form = Book.query.filter_by(id=id).first_or_404()
    form.like += 1
    db.session.commit()
    flash('Thumb up success!!', 'info')
    return render_template('show_book.html', form=form)

@web_bp.route('/delete/<int:id>/')
@login_required
def delete(id):
    form = Book.query.filter_by(id=id).first_or_404()
    db.session.delete(form)
    db.session.commit()
    flash('You have delete a book', 'info')
    return redirect(url_for('web.my_book'))

@web_bp.route('/change/<int:id>/', methods=['GET', 'POST'])
@login_required
def change_book(id):
    form = BookForm()
    book = Book.query.filter_by(id=id).first_or_404()
    if request.method == 'POST':
        if form.validate_on_submit():
            book = Book.query.filter_by(id=id).first_or_404()

            book.user_name = form.author.data
            book.title = form.title.data
            book.description = form.description.data

            if form.algorithms.data == True:
                book.tag.append(Tag.query.get(1))
            if form.programming.data == True:
                book.tag.append(Tag.query.get(2))
            if form.math.data == True:
                book.tag.append(Tag.query.get(3))
            if form.software.data == True:
                book.tag.append(Tag.query.get(4))
            if form.other.data == True:
                book.tag.append(Tag.query.get(5))

            db.session.commit()
            flash('You have successfully modify your book', 'info')
            return redirect(url_for('web.Show_book_list'))

        else:
            app.logger.info('%s failed to modification one book', current_user.username)
            flash("Sorry, the modification failed ! ", "error")

    form.author.data = book.user_name
    form.title.data = book.title
    form.description.data = book.description

    tags = []
    for tag in book.tag:
        tags.append(tag.name)

    if "algorithms" in tags:
        form.algorithms.data = True
    if "programming" in tags:
        form.programming.data = True
    if "math" in tags:
        form.math.data = True
    if "software" in tags:
        form.software.data = True
    if "other" in tags:
        form.other.data = True

    return render_template('modify.html', form=form)

@web_bp.route('/register/', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            user = User(
                username=form.username.data,
                password=generate_password_hash(form.password.data)
            )
            db.session.add(user)
            db.session.commit()
            flash("Thanks for registering", "success")
            return redirect(url_for('web.login'))

    return render_template('register.html', form=form)

@web_bp.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            username = form.username.data
            password = form.password.data
            user = User.query.filter_by(username=username).first()

            if user.check_password(password):
                login_user(user)
                session['username'] = username
                flash('you have logged in!', 'info')
                return redirect(url_for('web.Show_book_list'))
            else:
                flash('Invalid username or password', 'danger')

    return render_template('login.html', form=form)

@web_bp.route('/logout/')
@login_required
def logout():
    logout_user()
    session.pop("username")
    flash('you have logout!', 'info')
    return redirect(url_for('web.login'))


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=int(user_id)).first()

@web_bp.route('/set_cookie/')
def set_cookie():
    response = make_response('success')
    # set cookie - close and do nothing
    # max_age 'second'
    response.set_cookie('Itcast', 'Python', max_age=3600)
    return response

@web_bp.route("/get_cookie/")
def get_cookie():
    cookie = request.cookies.get("Itcast")
    return cookie

@web_bp.route("/delete_cookie/")
def delete_cookie():
    resp = make_response("del success")
    resp.delete_cookie("Itcast")
    return resp





