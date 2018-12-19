from flask import Flask,render_template,request,flash,redirect,url_for,jsonify
from sqlalchemy import create_engine, asc,desc
from sqlalchemy.orm import sessionmaker
from models import Base, Category, CategoryItem
app=Flask(__name__)


# Connect to Database and create database session
engine = create_engine('sqlite:///catalogapp.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

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
    return render_template('categoryitem.html',category_name=category_name,items=items,categories=categories)

@app.route('/catalog/<string:category_name>/<int:item_id>/')
def getItem(category_name,item_id):
    item=session.query(CategoryItem).filter_by(id=item_id).one()
    return render_template('item.html',category_name=category_name,item=item)

@app.route('/catalog/<string:category_name>/items/new/',methods=['GET','POST'])
def newCategoryItem(category_name):
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
