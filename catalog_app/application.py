from flask import Flask, render_template, request
from flask import redirect, jsonify, url_for, flash
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Book, User
from flask import session as login_session

import requests
import json
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
from flask import make_response
from flask_httpauth import HTTPBasicAuth

CLIENT_ID = json.loads(open('client_secrets.json', 'r')
                       .read())['web']['client_id']

app = Flask(__name__)
app.secret_key = 'super secret key'

# connect to database
engine = create_engine('sqlite:///category.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

auth = HTTPBasicAuth()
g = User()


@auth.verify_password
def verify_password(username, password):
    """
    Method to verify password from database when using local authentication.
    :param username: Value to lookup.
    :param password: Value to verify.
    :return: Boolean
    """
    user = session.query(User).filter_by(username=username).first()
    if not user or not user.verify_password(password):
        return False
    g.user = user
    return True


@app.route('/users', methods=['POST'])
def new_user():
    """
    Method to create a new user if not found.
    :return: JSON object with username.
    """
    username = request.json.get('username')
    password = request.json.get('password')
    name = request.json.get('name')
    email = request.json.get('email')
    if username is None or password is None:
        abort(400)
    if session.query(User).filter_by(username=username).first() is not None:
        abort(400)
    user = User(username=username, name=name, email=email)
    user.hash_password(password)
    session.add(user)
    session.commit()
    return jsonify({'username': user.username}), 201


@app.route('/protected_resource')
@auth.login_required
def get_resource():
    """
    Method to test local authentication.
    :return: JSON object with message/username.
    """
    return jsonify({'data': 'Hello, %s!' % g.user.username})


@app.route('/login')
def login():
    """
    Method to create a random string for authentication.
    :return: Returns the login.html page and state set with a random string.
    """
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in range(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)


@app.route('/clearSession')
def clear_session():
    """
    Method to clear the login session for local testing.
    :return: String message.
    """
    login_session.clear()
    return "Session cleared"


@app.route('/gconnect', methods=['POST'])
def gconnect():
    """
    Udacity method to enable google authentication.
    :return: Welcome page upon success and redirected to the home page.
    """
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print("Token's client ID does not match app's.")
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already '
                                            'connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    # check if user exists otherwise create a new user
    user_email = session.query(User)\
        .filter_by(email=login_session['email']).one_or_none()

    login_session['user_id'] = user_email.id

    if not user_email:
        user = User(username=login_session['username'],
                    picture=login_session['picture'],
                    email=login_session['email'])
        session.add(user)
        session.commit()

        flash('Created %s user.' % user.email)
        login_session['id'] = session.query(User)\
            .filter_by(email=user.email).one_or_none()

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 100px; height: 100px;border-radius: ' \
              '150px;-webkit-border-radius: 150px;-moz-border-radius: ' \
              '150px;">'
    flash("you are now logged in as %s" % login_session['username'])
    print("done!")
    return output


@app.route('/gdisconnect')
def gdisconnect():
    """
    Udacity method to disconnect from your google account
    :return: Redirect to homepage without being logged in otherwise a
    failure message.
    """
    access_token = login_session.get('access_token')
    if access_token is None:
        print('Access Token is None')
        response = make_response(json.dumps('Current user not connected.'),
                                 401)
        response.headers['Content-Type'] = 'application/json'
        # return response
        return redirect(url_for('show_categories'))
    print('In gdisconnect access token is %s', access_token)
    print('User name is: ')
    print(login_session['username'])
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' \
          % login_session['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print('result is ')
    print(result)
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        # return response
        return redirect(url_for('show_categories'))
    else:
        response = make_response(json.dumps('Failed to revoke token for '
                                            'given user.'), 400)
        response.headers['Content-Type'] = 'application/json'
        return response


@app.route('/', methods=['GET'])
def show_categories():
    """
    Method to show all existing categories.
    :return: List of categories and a redirect to home.html.
    """
    categories = session.query(Category).order_by(Category.name).all()
    return render_template('home.html', categories=categories)


@app.route('/category/create/', methods=['GET', 'POST'])
def create_category():
    """
    Method to create a new category.
    :return: Redirect to show categories on a POST, otherwise a redirect
     to category_modify.html.
    """
    if request.method == 'POST':
        category = Category(name=request.form['name'],
                            description=request.form['description'],
                            user_id=login_session['user_id'])
        session.add(category)
        session.commit()
        flash('Created %s category.' % category.name)
        return redirect(url_for('show_categories'))
    else:
        return render_template('category_modify.html')


@app.route('/category/<int:category_id>/update', methods=['GET', 'POST'])
def update_category(category_id):
    """
    Method to update a category.
    :param category_id: Category id to be updated.
    :return: Show the category and books on a POST, otherwise a redirect
     to category_modify.html.
    """
    category = session.query(Category).filter_by(id=category_id).one()
    if category.user_id != login_session['user_id']:
        flash('''You are not authorized to edit this item.
              Create your own item to edit.''')
        return redirect(url_for('show_category_books',
                                category_id=category_id))
    if request.method == 'POST':
        if request.form['name']:
            category.name = request.form['name']
        if request.form['description']:
            category.description = request.form['description']
            flash('Updated %s category.' % category.name)
        return redirect(url_for('show_category_books',
                                category_id=category_id))
    else:
        return render_template('category_modify.html', category_id=category_id,
                               category=category)


@app.route('/category/<int:category_id>/delete', methods=['GET', 'POST'])
def delete_category(category_id):
    """
    Method to delete a category and any associated books.
    :param category_id: Category id to be deleted.
    :return: Redirect to the homepage on a POST, otherwise a redirect
     to category_delete.html.
    """
    category = session.query(Category).filter_by(id=category_id).one()
    books = session.query(Book).filter_by(category_id=category_id).all()
    if category.user_id != login_session['user_id']:
        flash('''You are not authorized to edit this item.
              Create your own item to edit.''')
        return redirect(url_for('show_category_books',
                                category_id=category_id))

    if request.method == 'POST':
        if category is not None:
            for book in books:
                session.delete(book)
                flash('Deleted %s book..' % book.name)
                session.commit()
            session.delete(category)
            flash('Deleted %s category.' % category.name)
            session.commit()
        return redirect(url_for('show_categories'))
    else:
        return render_template('category_delete.html', category=category,
                               books=books)


@app.route('/category/<int:category_id>/book', methods=['GET'])
def show_category_books(category_id):
    """
    Method to show a category and associated books.
    :param category_id: Category id to be displayed.
    :return: Redirect to the category/books page on a POST, otherwise a
     redirect to book_modify.html.
    """
    category = session.query(Category).filter_by(id=category_id).first()
    books = session.query(Book).filter_by(category_id=category_id)\
        .order_by(Book.name).all()
    return render_template('category_books.html', category=category,
                           books=books)


@app.route('/category/<int:category_id>/book/create', methods=['GET', 'POST'])
def create_book(category_id):
    """
    Mehtod to create a new book in a category.
    :param category_id: Category id the book should be linked too.
    :return: Redirect to show the category and books on a POST, otherwise
     a redirect to book_modify.html.
    """
    category = session.query(Category).filter_by(id=category_id).first()
    if request.method == 'POST':
        book = Book(name=request.form['name'], author=request.form['author'],
                    category_id=category_id, user_id=login_session['user_id'])
        session.add(book)
        session.commit()
        flash('Created %s book.' % book.name)
        return redirect(url_for('show_category_books',
                                category_id=category_id))
    else:
        return render_template('book_modify.html', category=category)


@app.route('/category/<int:category_id>/book/<int:book_id>/update',
           methods=['GET', 'POST'])
def update_book(category_id, book_id):
    """
    Method to updatte a book.
    :param category_id: Category id the book is associated too.
    :param book_id: Book id to be updated.
    :return: Redirect to show the category/books on a POST, otherwise a
    redirect to book_modify.html.
    """
    category = session.query(Category).filter_by(id=category_id).one()
    book = session.query(Book).filter_by(id=book_id).one()

    if book.user_id != login_session['user_id']:
        flash('''You are not authorized to edit this item.
              Create your own item to edit.''')
        return redirect(url_for('show_category_books',
                                category_id=category_id))

    if request.method == 'POST':
        if request.form['name']:
            book.name = request.form['name']
        if request.form['author']:
            book.author = request.form['author']
        session.add(book)
        session.commit()
        flash('Updated %s book.' % book.name)
        return redirect(url_for('show_category_books',
                                category_id=category_id))
    else:
        return render_template('book_modify.html', category=category,
                               book=book)


@app.route('/category/<int:category_id>/book/<int:book_id>/delete',
           methods=['GET', 'POST'])
def delete_book(category_id, book_id):
    """
    Method to delete a book.
    :param category_id: Category id the book is associated to.
    :param book_id: Book id to be deleted.
    :return: Redirect to show the category/books.
    """
    book = session.query(Book).filter_by(id=book_id).one()

    if book.user_id != login_session['user_id']:
        flash('''You are not authorized to edit this item.
              Create your own item to edit.''')
        return redirect(url_for('show_category_books',
                                category_id=category_id))

    if request.method == 'POST':
        session.delete(book)
        session.commit()
        flash('Deleted %s book.' % book.name)
    return redirect(url_for('show_category_books', category_id=category_id))


@app.route('/categories/api')
def api_categories():
    """
    Method to display all the categories.
    :return: JSON list of categories.
    """
    categories = session.query(Category).order_by(Category.name).all()
    categories_json = [c.serialize for c in categories]
    return jsonify(Category=categories_json)


@app.route('/books/api')
def api_books():
    """
    Method to display all the books.
    :return: JSON list of all books.
    """
    books = session.query(Book).order_by(Book.name).all()
    books_json = [i.serialize for i in books]
    return jsonify(Book=books_json)


@app.route('/category/<int:category_id>/book/<int:book_id>/api')
def api_category_books(category_id, book_id):
    """
    Method to display a category and associated books.
    :return: JSON list of categories/books.
    """
    category = session.query(Category).filter_by(id=category_id).one_or_none()
    if category is not None:
        category_json = category.serialize
        if len(category_json) != 0:
            book = session.query(Book)\
                .filter_by(category_id=category_id, id=book_id).one_or_none()
            if book is not None:
                book_json = book.serialize

                if len(book_json) != 0:
                    category_json["Books"] = book_json
    else:
        category_json = {}
    return jsonify(Category=category_json)


@app.route('/category/books/api')
def api_all_category_books():
    """
    Method to display all categories and associated books.
    :return: JSON list of categories/books.
    """
    categories = session.query(Category).order_by(Category.name).all()
    categories_json = [c.serialize for c in categories]
    for c in range(len(categories_json)):
        books = session.query(Book)\
            .filter_by(category_id=categories_json[c]['id']).all()
        books_json = [i.serialize for i in books]

        if len(books_json) != 0:
            categories_json[c]["Books"] = books_json
    return jsonify(Category=categories_json)


@app.route('/users/api')
def api_users():
    """
    Method to display all users.
    :return: JSON list of all users.
    """
    users = session.query(User).order_by(User.email).all()
    users_json = [i.serialize for i in users]
    return jsonify(User=users_json)

# todo Code is ready for personal review and neatly formatted and
#  compliant with the Python PEP 8 style guide.
# todo README file includes details of all the steps required to
#  successfully run the application.


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000, threaded=False)
