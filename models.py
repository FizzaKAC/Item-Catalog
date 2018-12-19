from sqlalchemy import Column, ForeignKey, Integer, String,DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
import datetime

Base = declarative_base()

class Category(Base):
    __tablename__='category'

    id=Column(Integer,primary_key=True)
    name=Column(String(80),nullable=False)
    items=relationship('CategoryItem',backref='category',lazy=True)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        list=[]
        for item in self.items:
           list.append(item.serialize)
        return {
            'id':self.id,
            'name':self.name,
            'items':list
        }

class CategoryItem(Base):
    __tablename__='category_item'

    id=Column(Integer,primary_key=True)
    name=Column(String(250),nullable=False)
    description=Column(String(250))
    price=Column(String(8))
    created_date = Column(DateTime, default=datetime.datetime.utcnow)
    category_id=Column(Integer,ForeignKey('category.id'),nullable=False)
    #category=relationship(Category)

    @property
    def serialize(self):
         """Return object data in easily serializeable format"""
         return{
             'id':self.id,
             'name':self.name,
             'description':self.description,
             'price':self.price,
             'created_date':self.created_date,
             'category':self.category.name
         }


engine = create_engine('sqlite:///catalogapp.db')
Base.metadata.create_all(engine)
