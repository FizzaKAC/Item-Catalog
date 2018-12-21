from flask import Flask,render_template,request,flash,redirect,url_for,jsonify
from sqlalchemy import create_engine, asc,desc
from sqlalchemy.orm import sessionmaker
from models import Base, Category, CategoryItem,User


from flask_httpauth import HTTPBasicAuth
import json
from flask import session as login_session
import random
import string

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
from flask import make_response
import requests

app=Flask(__name__)
CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Item Catalog"

# Connect to Database and create database session
engine = create_engine('sqlite:///catalogapp.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# Create anti-forgery state token
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    # return "The current session state is %s" % login_session['state']
    return render_template('login.html', STATE=state)

@app.route('/oauth/<provider>',methods=['POST'])
def login(provider):
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    auth_code=request.json.get('item')
    if provider =='google':
        try:
            # Upgrade the authorization code into a credentials object
            oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
            oauth_flow.redirect_uri = 'postmessage'
            credentials = oauth_flow.step2_exchange(auth_code)
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
            print "Token's client ID does not match app's."
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


        login_session['provider'] = 'google'
        # see if user exists, if it doesn't make a new one
        user= getUser(data["email"])
        if not user:
            user = createUser(login_session)
        login_session['user_id'] = user.id
        
        #make token
        token = user.generate_auth_token()

        
        flash("You are now logged in as %s" % login_session['username'])
        #send back token to the client 
        return redirect(url_for('index'))
        
        #return jsonify({'token': token.decode('ascii'), 'duration': 600})
    else:
        return 'Unrecoginized Provider'


@app.route("/logout")
def logout():
    if 'provider' in login_session:
        if login_session['provider'] == 'google':
            gdisconnect()
            del login_session['gplus_id']
            del login_session['access_token']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        del login_session['user_id']
        del login_session['provider']
        flash("You have successfully been logged out.")
        return redirect(url_for('index'))
    else:
        flash("You were not logged in")
        return redirect(url_for('index'))

def gdisconnect():
    # Only disconnect a connected user.
    access_token = login_session.get('access_token')
    print access_token
    if access_token is None:
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    if result['status'] == '200':
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        print result
        response = make_response(json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response
    
def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    #user = session.query(User).filter_by(email=login_session['email']).one()
    return newUser

def getUser(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user
    except:
        return None
@app.route('/catalog/<string:category_name>/<int:item_id>/JSON')
def itemJSON(category_name,item_id):
    item=session.query(CategoryItem).filter_by(id=item_id).one()
    return jsonify(Category_Item=item.serialize)

@app.route('/catalog/JSON')
def catalogJSON():
    categories=session.query(Category).all()
    return jsonify(catalog=[c.serialize for c in categories]
    )

@app.route('/')
@app.route('/catalog/')
def index():
    categories=session.query(Category).order_by(asc(Category.name))
    recentItems=session.query(CategoryItem).order_by(desc(CategoryItem.created_date)).limit(10).all()
    return render_template('index.html',categories=categories,items=recentItems)

@app.route('/catalog/<string:category_name>/')
@app.route('/catalog/<string:category_name>/items/')
def showItems(category_name):
    #category=session.query(Category).filter_by(name=category_name).one()
    categories=session.query(Category).order_by(asc(Category.name))
    items=session.query(CategoryItem).join(Category).filter(Category.name==category_name).all()
    #print category.id
    if 'username' not in login_session:
        return render_template('publiccategoryitem.html',category_name=category_name,items=items,categories=categories)
    else:
        return render_template('categoryitem.html',category_name=category_name,items=items,categories=categories)
    

@app.route('/catalog/<string:category_name>/<int:item_id>/')
def getItem(category_name,item_id):
    item=session.query(CategoryItem).filter_by(id=item_id).one()
    if 'username' not in login_session:
        return render_template('publicitem.html',category_name=category_name,item=item)
    else:
        return render_template('item.html',category_name=category_name,item=item)

@app.route('/catalog/<string:category_name>/items/new/',methods=['GET','POST'])
def newCategoryItem(category_name):
    if 'username' not in login_session:
        return redirect('/login')
    category=session.query(Category).filter_by(name=category_name).one()
    #print category.name
    if request.method == 'POST':
        newItem=CategoryItem(name=request.form['name'],description=request.form['description'],price=request.form['price'],category_id=category.id)
        session.add(newItem)
        session.commit()
        flash('New Menu %s Item Successfully Created' % (newItem.name))
        return redirect(url_for('showItems', category_name=category_name))
    else:
        return render_template('newcategoryitem.html')

@app.route('/catalog/<string:category_name>/items/<int:item_id>/edit/',methods=['GET','POST'])
def editCategoryItem(category_name,item_id):
    if 'username' not in login_session:
        return redirect('/login')
    editedItem=session.query(CategoryItem).filter_by(id=item_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
        if request.form['description']:
            editedItem.description = request.form['description']
        if request.form['price']:
            editedItem.price = request.form['price']
        session.add(editedItem)
        session.commit()
        flash('Category Item Successfully Edited')
        return redirect(url_for('showItems', category_name=category_name))
    else:
        return render_template('editcategoryitem.html',item=editedItem,category_name=category_name)

@app.route('/catalog/<string:category_name>/items/<int:item_id>/delete',methods=['GET','POST'])
def deleteCategoryItem(category_name,item_id):
    if 'username' not in login_session:
        return redirect('/login')
    itemToDelete=session.query(CategoryItem).filter_by(id=item_id).one()
    if request.method=='POST':
        flash(itemToDelete.name+' successfully deleted')
        session.delete(itemToDelete)
        session.commit()
        return redirect(url_for('showItems',category_name=category_name))
    else:
        return render_template('deletecategoryitem.html',item=itemToDelete,category_name=category_name)

if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000,threaded=False)
