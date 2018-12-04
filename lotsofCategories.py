from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Category, Base, CategoryItem

engine = create_engine('sqlite:///catalogapp.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)

session = DBSession()


category1 = Category(name = "Incandescent lamps")

session.add(category1)
session.commit()


category2 = Category(name = "Compact fluorescent lamps")

session.add(category2)
session.commit()


category3 = Category(name = "Halogen lamps")

session.add(category3)
session.commit()


category4 = Category(name = "Metal halide Lamps")

session.add(category4)
session.commit()


category5 = Category(name = "Light Emitting Diode ")

session.add(category5)
session.commit()


category6 = Category(name = "Fluorescent tube")

session.add(category6)
session.commit()


category7 = Category(name = "Neon lamps")

session.add(category7)
session.commit()


category8 = Category(name = "High intensity discharge lamps")

session.add(category8)
session.commit()


category9=Category(name="Low pressure sodium lamps")

session.add(category9)
session.commit()

print "added categories!"
