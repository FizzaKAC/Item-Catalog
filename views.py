from flask import Flask,render_template
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from models import Base, Category, CategoryItem
app=Flask(__name__)


# Connect to Database and create database session
engine = create_engine('sqlite:///catalogapp.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/')
@app.route('/catalog/')
def index():
    categories=session.query(Category).order_by(asc(Category.name))
    return render_template('categories.html',categories=categories)

@app.route('/catalog/<string:category_name>/')
@app.route('/catalog/<string:category_name>/items/')
def showItems(category_name):
    category=session.query(Category).filter_by(name=category_name).one()
    items=session.query(CategoryItem).filter_by(category_id=category.id).all()
    print category.id
    return render_template('menu.html',category=category,items=items)

@app.route('/catalog/<string:category_name>/items/new',methods=['GET','POST'])
def newCategoryItem(category_name):
    category=session.query(Category).filter_by(name=category_name).one()
    print category.name
    return 'inside'

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000,threaded=False)
