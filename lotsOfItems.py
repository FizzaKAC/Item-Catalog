from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Category, Base, CategoryItem, User

engine = create_engine('sqlite:///catalogapp.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)

session = DBSession()

item1 = CategoryItem(name="lamp1", description="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Mauris facilisis, felis at cursus auctor, nibh est pretium est, quis aliquet risus ligula ut quam. Orci varius natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Vestibulum et est mauris. Etiam ultrices velit sed vehicula malesuada.", price=10, category_id=1)
session.add(item1)
session.commit()

item2 = CategoryItem(name="lamp2", description="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Mauris facilisis, felis at cursus auctor, nibh est pretium est, quis aliquet risus ligula ut quam. Orci varius natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Vestibulum et est mauris. Etiam ultrices velit sed vehicula malesuada.", price=8, category_id=1)
session.add(item2)
session.commit()

item3 = CategoryItem(name="lamp3", description="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Mauris facilisis, felis at cursus auctor, nibh est pretium est, quis aliquet risus ligula ut quam. Orci varius natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Vestibulum et est mauris. Etiam ultrices velit sed vehicula malesuada.", price=12, category_id=2)
session.add(item3)
session.commit()

item4 = CategoryItem(name="lamp4", description="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Mauris facilisis, felis at cursus auctor, nibh est pretium est, quis aliquet risus ligula ut quam. Orci varius natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Vestibulum et est mauris. Etiam ultrices velit sed vehicula malesuada.", price=5, category_id=2)
session.add(item4)
session.commit()

item5 = CategoryItem(name="lamp5", description="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Mauris facilisis, felis at cursus auctor, nibh est pretium est, quis aliquet risus ligula ut quam. Orci varius natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Vestibulum et est mauris. Etiam ultrices velit sed vehicula malesuada.", price=10, category_id=2)
session.add(item5)
session.commit()

item6 = CategoryItem(name="lamp6", description="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Mauris facilisis, felis at cursus auctor, nibh est pretium est, quis aliquet risus ligula ut quam. Orci varius natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Vestibulum et est mauris. Etiam ultrices velit sed vehicula malesuada.", price=7, category_id=3)
session.add(item6)
session.commit()

item7 = CategoryItem(name="lamp7", description="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Mauris facilisis, felis at cursus auctor, nibh est pretium est, quis aliquet risus ligula ut quam. Orci varius natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Vestibulum et est mauris. Etiam ultrices velit sed vehicula malesuada.", price=15, category_id=4)
session.add(item7)
session.commit()

item8 = CategoryItem(name="lamp8", description="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Mauris facilisis, felis at cursus auctor, nibh est pretium est, quis aliquet risus ligula ut quam. Orci varius natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Vestibulum et est mauris. Etiam ultrices velit sed vehicula malesuada.", price=12, category_id=5)
session.add(item8)
session.commit()

item9 = CategoryItem(name="lamp9", description="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Mauris facilisis, felis at cursus auctor, nibh est pretium est, quis aliquet risus ligula ut quam. Orci varius natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Vestibulum et est mauris. Etiam ultrices velit sed vehicula malesuada.", price=18, category_id=6)
session.add(item9)
session.commit()
print "Added Items!"  