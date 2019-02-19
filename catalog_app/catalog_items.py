from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, Catalog, CatalogItem


engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

catalog1 = Catalog(name='Snowboarding')
session.add(catalog1)
session.commit()
catalogItem1 = CatalogItem(name='Board', description='This is a snow board', catalog=catalog1)
session.add(catalogItem1)
session.commit()

catalog2 = Catalog(name='Bowling')
session.add(catalog2)
session.commit()
catalogItem2 = CatalogItem(name='Ball', description='This is a bowling ball', catalog=catalog2)
session.add(catalogItem2)
session.commit()

print('Added all catalogs and items.')
