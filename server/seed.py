#!/usr/bin/env python3

from random import choice as rc

from faker import Faker
from sqlalchemy import func

from app import app
from models import db, Author, Post


fake = Faker()

with app.app_context():

    Author.query.delete()
    Post.query.delete()

    authors = []
    for n in range(25):
        author = Author(name=fake.name(), phone_number='1324543333')
        authors.append(author)

    db.session.add_all(authors)
    posts = []
    for n in range(25):
        post = Post(title='Secret banana', content='This is the content Secret' * 50, category= 'Fiction', summary="Summary Secret" )
        posts.append(post)

    db.session.add_all(posts)

    db.session.commit()
    

    # Find all authors with duplicate names
    duplicates = db.session.query(Author.name, func.count(Author.id).label('count')).group_by(Author.name).having(func.count(Author.id) > 1).all()

    # Loop through the duplicates and delete all but the first record for each name
    for name, count in duplicates:
        authors = db.session.query(Author).filter_by(name=name).all()
        for author in authors[1:]:
            db.session.delete(author)

    # Commit the changes
    db.session.commit()