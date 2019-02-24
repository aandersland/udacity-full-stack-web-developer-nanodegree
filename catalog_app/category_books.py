from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, User, Category, Book

engine = create_engine('sqlite:///category.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

user1 = User(name='Elmer Fudd', email='elmerfudd@acme.com')
session.add(user1)
session.commit()

user2 = User(name='Bugs Bunny', email='bugsbunny@acme.com')
session.add(user2)
session.commit()

user3 = User(name='Daffy Duck', email='daffyduck@acme.com')
session.add(user3)
session.commit()

category1 = Category(name='Science Fiction',
                     description='Science fiction (often shortened to Sci-Fi' 
                                 ' or SF) is a genre of speculative fiction, '
                                 'typically dealing with imaginative concepts'
                                 ' such as advanced science and technology, '
                                 'space exploration, time travel, and '
                                 'extraterrestrial life.',
                     user_id=user1.id)
session.add(category1)
session.commit()

book1 = Book(name='A Space Odyssey', author='Arthur C. Clarke',
             category=category1, user_id=user1.id)
session.add(book1)
session.commit()

book2 = Book(name='Dune', author='Frank Herbert', category=category1,
             user_id=user1.id)
session.add(book2)
session.commit()

book3 = Book(name='The Hitchhicker\'s Guide to the Galaxy',
             author='Douglas Adams', category=category1,
             user_id=user1.id)
session.add(book3)
session.commit()

category2 = Category(
    name='Fiction',
    description ='Fiction broadly refers to any narrative that is derived from the im'
         'agination-in other words, not based strictly on history or fact. It'
         ' can also refer, more narrowly, to narratives written only in prose'
         ' (the novel and short story), and is often used as a synonym for the'
         ' novel.',
    user_id=user2.id)
session.add(category2)
session.commit()

book4 = Book(name='The Da Vinci Code', author='Dan Brown', category=category2,
             user_id=user2.id)
session.add(book4)
session.commit()

book5 = Book(name='The Hobbit', author='J.R.R. Tolkien', category=category2,
             user_id=user2.id)
session.add(book5)
session.commit()

book6 = Book(name='The Catcher in the Rye', author='J.D. Salinger',
             category=category2, user_id=user2.id)
session.add(book6)
session.commit()

category3 = Category(name='Fantasy',
                     description='Fantasy is a genre of speculative fiction '
                                 'set in a fictional universe, often without '
                                 'any locations, events, or people '
                                 'referencing the real world. Its roots are '
                                 'in oral traditions, which then became '
                                 'literature and drama. From the twentieth '
                                 'century it has expanded further into various'
                                 ' media, including film, television, graphic'
                                 ' novels and video games.',
                     user_id=user3.id)
session.add(category3)
session.commit()

book7 = Book(name='The Eye of the World', author='Robert Jordon',
             category=category3, user_id=user3.id)
session.add(book7)
session.commit()

book8 = Book(name='The Great Hunt', author='Robert Jordon',
             category=category3, user_id=user3.id)
session.add(book8)
session.commit()

book9 = Book(name='The Dragon Reborn', author='Robert Jordon',
             category=category3, user_id=user3.id)
session.add(book9)
session.commit()

print('Added all categories and books.')
