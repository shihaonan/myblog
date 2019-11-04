from app.models import *
from app.extentions import db
from faker import Faker
import random
from sqlalchemy.exc import IntegrityError

def fake_admin():
    admin = Admin(
        username='haonan'
    )
    # admin.set_password('lalalala')
    db.session.add(admin)
    db.session.commit()

def fake_bloginfo():
    bloginfo = Bloginfo(
        blog_title='我的博客',
        blog_sub_title = '这是我的地盘',
        name = '施浩楠',
        about = '蜀道之难，难于上青天'
    )
    db.session.add(bloginfo)
    db.session.commit()

fake = Faker('zh_CN')

def fake_categories(count=10):
    categoty = Category(name='默认')
    db.session.add(categoty)

    for i in range(count):
        categoty = Category(name = fake.word())
        db.session.add(categoty)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()

def fake_posts(count=50):
    for i in range(count):
        post = Post(
            title=fake.sentence(),
            body=fake.text(2000),
            category=Category.query.get(random.randint(1,
Category.query.count())),
            timestamp=fake.date_time_this_year()
        )
        db.session.add(post)
    db.session.commit()

def fake_comments(count=500):
    for i in range(count):
        comment = Comment(
            author=fake.name(),
            email=fake.email(),
            site=fake.url(),
            body=fake.sentence(),
            timestamp=fake.date_time_this_year(),
            reviewed=True,
            post=Post.query.get(random.randint(1, Post.query.count()))
        )
        db.session.add(comment)

    salt = int(count * 0.1)
    for i in range(salt):
        # 未审核评论
        comment = Comment(
            author=fake.name(),
            email=fake.email(),
            site=fake.url(),
            body=fake.sentence(),
            timestamp=fake.date_time_this_year(),
            reviewed=False,
            post=Post.query.get(random.randint(1, Post.query.count()))
        )
        db.session.add(comment)

        # 管理员发表的评论
        comment = Comment(
            author='Mima Kirigoe',
            email='mima@example.com',
            site='example.com',
            body=fake.sentence(),
            timestamp=fake.date_time_this_year(),
            from_admin=True,
            reviewed=True,
            post=Post.query.get(random.randint(1, Post.query.count()))
        )
        db.session.add(comment)
    db.session.commit()

    # 回复
    for i in range(salt):
        comment = Comment(
            author=fake.name(),
            email=fake.email(),
            site=fake.url(),
            body=fake.sentence(),
            timestamp=fake.date_time_this_year(),
            reviewed=True,
            replied=Comment.query.get(random.randint(1,Comment.query.count())),
            post=Post.query.get(random.randint(1, Post.query.count())))
        db.session.add(comment)
    db.session.commit()








