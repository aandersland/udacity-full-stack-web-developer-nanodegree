from flask import Flask, render_template, request, redirect, jsonify, url_for, flash
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Catalog, CatalogItem
from flask import session as login_session

import requests
import json
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
from flask import make_response

CLIENT_ID = json.loads(open('client_secrets.json', 'r').read())['web']['client_id']

app = Flask(__name__)
app.secret_key = 'super secret key'

# connect to database
engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/login')
def login():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in range(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)


@app.route('/clearSession')
def clear_session():
    login_session.clear()
    return "Session cleared"


@app.route('/gconnect', methods=['POST'])
def gconnect():
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
        response = make_response(json.dumps('Current user is already connected.'),
                                 200)
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

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print("done!")
    return output


@app.route('/', methods=['GET'])
@app.route('/catalog/', methods=['GET'])
def show_catalogs():
    catalogs = session.query(Catalog).order_by(Catalog.name)
    items = session.query(CatalogItem).order_by(CatalogItem.name).all()
    return render_template('mainbody.html', catalogs=catalogs, items=items)


@app.route('/catalog/search/', methods=['GET'])
def search_catalog():
    catalog_name = request.args.get('catalog_name')
    catalog = session.query(Catalog).filter_by(name=catalog_name).first()
    return render_template('catalog.html', catalog=catalog)


@app.route('/catalog/<string:catalog_id>/', methods=['GET'])
def show_catalog(catalog_id):
    if catalog_id is not None:
        catalog = session.query(Catalog).filter_by(id=catalog_id).first()
    return render_template('catalog.html', catalog=catalog)


@app.route('/catalog/create/', methods=['GET', 'POST'])
def create_catalog():
    if request.method == 'POST':
        catalog = Catalog(name=request.form['name'], description=request.form['description'])
        session.add(catalog)
        session.commit()
        flash('Catalog %s created.' % catalog.name)
        return redirect(url_for('show_catalogs'))
    else:
        return render_template('createcatalog.html')


@app.route('/catalog/<int:catalog_id>/update', methods=['GET', 'POST'])
def update_catalog(catalog_id):
    catalog = session.query(Catalog).filter_by(id=catalog_id).one()
    if request.method == 'POST':
        if request.form['name']:
            catalog.name = request.form['name']
        if request.form['description']:
            catalog.description = request.form['description']
            flash('Catalog %s is updated.' % catalog.name)
        return redirect(url_for('show_catalogs'))
    else:
        return render_template('updatecatalog.html', catalog_id=catalog_id, catalog=catalog)


@app.route('/catalog/<int:catalog_id>/delete', methods=['GET', 'POST'])
def delete_catalog(catalog_id):
    catalog = session.query(Catalog).filter_by(id=catalog_id).one()
    if request.method == 'POST':
        if catalog is not None:
            session.delete(catalog)
            flash('%s successfully deleted.' % catalog.name)
            session.commit()
        return redirect(url_for('show_catalogs'))
    else:
        return render_template('deletecatalog.html', catalog_id=catalog_id, catalog=catalog)


# @app.route('/catalog/<int:catalog_id>/')
@app.route('/catalog/<int:catalog_id>/items', methods=['GET'])
def show_items(catalog_id):
    catalog = session.query(Catalog).filter_by(id=catalog_id).one()
    items = session.query(CatalogItem).filter_by(catalog_id=catalog_id).all()
    return render_template('catalogitems.html', catalog_id=catalog_id, catalog=catalog, catalog_items=items)


@app.route('/catalog/<int:catalog_id>/item/<int:item_id>', methods=['GET'])
def show_item(catalog_id, item_id):
    catalog = session.query(Catalog).filter_by(id=catalog_id).one()
    item = session.query(CatalogItem).filter_by(catalog_id=catalog_id, id=item_id).first()
    return render_template('catalogitem.html', catalog_id=catalog_id, catalog=catalog, catalog_item=item)


@app.route('/catalog/<int:catalog_id>/item/create', methods=['GET', 'POST'])
def create_item(catalog_id):
    catalog = session.query(Catalog).filter_by(id=catalog_id).one()
    if request.method == 'POST':
        catalogitem = CatalogItem(name=request.form['name'], description=request.form['description'],
                                  catalog_id=catalog_id)
        session.add(catalogitem)
        session.commit()
        flash('%s item is created.' % catalogitem.name)
        return redirect(url_for('show_items', catalog_id=catalog_id))
    else:
        return render_template('createcatalogitem.html', catalog_id=catalog_id)


@app.route('/catalog/<int:catalog_id>/item/<int:item_id>/update', methods=['GET', 'POST'])
def update_item(catalog_id, item_id):
    catalog = session.query(Catalog).filter_by(id=catalog_id).one()
    item = session.query(CatalogItem).filter_by(id=item_id).one()

    if request.method == 'POST':
        if request.form['name']:
            item.name = request.form['name']
        if request.form['description']:
            item.description = request.form['description']
        session.add(item)
        session.commit()
        flash('Catalog item successfully updated.')
        return redirect(url_for('show_items', catalog_id=catalog_id))
    else:
        return render_template('updatecatalogitem.html', catalog_id=catalog_id, item_id=item_id, item=item)


@app.route('/catalog/<int:catalog_id>/item/<int:item_id>/delete', methods=['GET', 'POST'])
def delete_item(catalog_id, item_id):
    catalog = session.query(Catalog).filter_by(id=catalog_id).one()
    item = session.query(CatalogItem).filter_by(id=item_id).one()
    if request.method == 'POST':
        session.delete(item)
        session.commit()
        flash('Catalog item successfully deleted.')
        return redirect(url_for('show_items', catalog_id=catalog_id))
    else:
        return render_template('deletecatalogitem.html', catalog_id=catalog_id, item=item)


# api json routes
@app.route('/catalog/api')
def json_catalogs():
    catalogs = session.query(Catalog).all()
    catalogs_json = [c.serialize for c in catalogs]
    for c in range(len(catalogs_json)):
        items = session.query(CatalogItem).filter_by(catalog_id=catalogs_json[c]['id']).all()
        items_json = [i.serialize for i in items]

        if len(items_json) != 0:
            catalogs_json[c]["CatalogItem"] = items_json

    return jsonify(Catalog=catalogs_json)


@app.route('/items/api')
def json_items():
    items = session.query(CatalogItem).all()
    items_json = [c.serialize for c in items]
    return jsonify(CatalogItem=items_json)


@app.route('/catalogs/api/<string:category_name>')
def json_get_catalog(category_name):
    catalog = session.query(Catalog).filter_by(name=category_name).one_or_none()
    catalog_json = None
    if catalog is not None:
        catalog_json = catalog.serialize

        items = session.query(CatalogItem).filter_by(catalog_id=catalog_json['id']).all()
        items_json = [i.serialize for i in items]

        if len(items) != 0:
            catalog_json["CatalogItem"] = items_json

    return jsonify(Catalog=catalog_json)


@app.route('/catalogs/api/<string:category_name>/<string:item_name>')
def json_get_item(category_name, item_name):
    catalog = session.query(Catalog).filter_by(name=category_name).one_or_none()
    if catalog is not None:
        item = session.query(CatalogItem).filter_by(catalog_id=catalog.id, name=item_name).one_or_none()
        if item is not None:
            item_json = item.serialize

    return jsonify(CatalogItem=item_json)


# The project implements a JSON endpoint that serves the same information as displayed in the HTML endpoints for an arbitrary item in the catalog.
# Website reads category and item information from a database.
# Website includes a form allowing users to add new items and correctly processes submitted forms.
# Website does include a form to edit/update a current record in the database table and correctly processes submitted forms.
# Website does include a function to delete a current record.
# todo Create, delete and update operations do consider authorization status prior to execution.
# todo Page implements a third-party authentication & authorization service (like Google Accounts or Mozilla Persona) instead of implementing its own authentication & authorization spec.
# todo Make sure there is a 'Login' and 'Logout' button/link in the project. The aesthetics of this button/link is up to the discretion of the student.
# todo Code is ready for personal review and neatly formatted and compliant with the Python PEP 8 style guide.
# todo Comments are present and effectively explain longer code procedures.
# todo README file includes details of all the steps required to successfully run the application.

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000, threaded=False)
