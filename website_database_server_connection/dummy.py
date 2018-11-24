import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from tabledef import *

engine = create_engine('sqlite:///website_users.db')

Session = sessionmaker(bind=engine)
session = Session()

user = User("kainaat", "Kai")
session.add(user)

user = User("aman", "a-man")
session.add(user)

user = User("himani", "hims")
session.add(user)

user = User("riyanka", "rinku")
session.add(user)

session.commit()
