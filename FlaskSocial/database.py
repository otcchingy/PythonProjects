import datetime
from sqlalchemy.dialects.postgresql import JSONB
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy



db = SQLAlchemy()


class Users(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True)
    password = db.Column(db.String(120))
    firstname = db.Column(db.String(32))
    lastname = db.Column(db.String(32))
    profile_pic = db.Column(db.String(80), nullable=True)
    dateofbirth = db.Column(db.Date)
    phone = db.Column(db.String(13), unique=True)
    email = db.Column(db.String(60), unique=True)
    confirmed_email = db.Column(db.String(4), nullable=True)
    confirmed_phone = db.Column(db.String(4), nullable=True)
    about = db.Column(db.String(3000), nullable=True)
    gender = db.Column(db.String(7), nullable=True)
    status = db.Column(db.Integer, nullable=True)
    user_status = db.Column(db.String(10))

    def __init__(self, firstname, lastname, username, password, phone, email, dateofbirth, about, user_status):
        self.firstname = firstname
        self.lastname = lastname
        self.username = username
        self.password = password
        self.dateofbirth = dateofbirth
        self.phone = phone
        self.email = email
        self.about = about
        self.user_status = user_status

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return (self.id)

    def __repr__(self):
        return (str(self.username))


class Friends(UserMixin, db.Model):
    __tablename__ = 'friends'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    friend_id = db.Column(db.Integer)
    add_code = db.Column(db.String(30), nullable=False)
    pending = db.Column(db.String(4), nullable=True, default='true')

    def __init__(self, user_id, friend_id, pending, add_code):
        self.friend_id = friend_id
        self.user_id = user_id
        self.pending = pending
        self.add_code = add_code


class Messages(UserMixin, db.Model):
    __tablename__ = 'messages'
    message_id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer)
    receiver_id = db.Column(db.Integer)
    message_content = db.Column(JSONB(), nullable=False)
    seen = db.Column(db.Integer, default=0)
    edited = db.Column(db.String(4), nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.datetime.now())

    def __init__(self, sender_id, receiver_id, message_content, timestamp):
        self.sender_id = sender_id
        self.message_content = message_content
        self.receiver_id = receiver_id
        self.timestamp = timestamp


class Group_Messages(UserMixin, db.Model):
    __tablename__ = 'group_messages'
    gmessage_id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer)
    group_id = db.Column(db.Integer)
    message_content = db.Column(JSONB(), nullable=False)
    seen = db.Column(db.Integer, default=0)
    edited = db.Column(db.String(4), nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.datetime.now())

    def __init__(self, sender_id, reciever_id, content, timestamp):
        self.sender_id = sender_id
        self.message_content = content
        self.reciever_id = reciever_id
        self.timestamp = timestamp


class Unread_Messages(UserMixin, db.Model):
    __tablename__ = 'unread_messages'
    unread_id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer)
    receiver_id = db.Column(db.Integer)
    count = db.Column(db.Integer, default=0)

    def __init__(self, sender_id, receiver_id, count):
        self.sender_id = sender_id
        self.receiver_id = receiver_id
        self.count = count
        


class Comments(UserMixin, db.Model):
    __tablename__ = 'comments'
    comment_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    post_id = db.Column(db.Integer)
    comment_content = db.Column(JSONB(), nullable=False)
    edited = db.Column(db.String(4), nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.datetime.now())

    def __init__(self, user_id, post_id, comment_content, timestamp):
        self.user_id = user_id
        self.post_id = post_id
        self.comment_content = comment_content
        self.timestamp = timestamp


class Follows(UserMixin, db.Model):
    __tablename__ = 'follows'
    id = db.Column(db.Integer, primary_key=True)
    follower = db.Column(db.Integer)
    following = db.Column(db.Integer)
    add_code = db.Column(db.String(30), nullable=False)

    def __init__(self, follower, following, add_code):
        self.follower = follower
        self.following = following
        self.add_code = add_code



class Posts(UserMixin, db.Model):
    __tablename__ = 'posts'
    post_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    post_content = db.Column(JSONB())
    # post_content = db.Column(db.String(3000), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.datetime.now())
    privacy = db.Column(db.String(8), default='public')
    edited = db.Column(db.String(4), nullable=True)

    def __init__(self, user_id, post_content, privacy, timestamp):
        self.user_id = user_id
        self.post_content = post_content
        self.privacy = privacy
        self.timestamp = timestamp


class Gallery(UserMixin, db.Model):
    __tablename__ = 'gallery'
    gallery_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    upload_type = db.Column(db.String(8))
    upload_used_as = db.Column(db.String(20))
    upload_path = db.Column(JSONB())
    privacy = db.Column(db.String(8), default='public')
    timestamp = db.Column(db.DateTime, default=datetime.datetime.now())

    def __init__(self, upload_type, upload_path, upload_used_as, user_id, privacy, timestamp):
        self.gallery_type = upload_type
        self.user_id = user_id
        self.upload_type = upload_type
        self.upload_used_as = upload_used_as
        self.upload_path = upload_path
        self.privacy = privacy
        self.timestamp = timestamp


class Likes(UserMixin, db.Model):
    __tablename__ = 'likes'
    like_id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, nullable=False)
    liker = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.datetime.now())

    def __init__(self, post_id, liker, timestamp):
        self.post_id = post_id
        self.liker = liker
        self.timestamp = timestamp


class Comment_likes(UserMixin, db.Model):
    __tablename__ = 'comment_likes'
    like_id = db.Column(db.Integer, primary_key=True)
    comment_id = db.Column(db.Integer, nullable=False)
    liker = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.datetime.now())

    def __init__(self, comment_id, liker, timestamp):
        self.comment_id = comment_id
        self.liker = liker
        self.timestamp = timestamp


class Notifications(UserMixin, db.Model):
    __tablename__ = 'notifications'
    note_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    sender_name = db.Column(db.String(32))
    note_header = db.Column(db.String(4))
    note_content = db.Column(JSONB())
    note_receiver = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime, default=datetime.datetime.now())
    seen = db.Column(db.String(1), nullable=True)

    def __init__(self, user_id, sender_name, note_header, note_content, note_receiver, timestamp):
        self.user_id = user_id
        self.note_header = note_header
        self.note_content = note_content
        self.note_receiver = note_receiver
        self.timestamp = timestamp
        self.sender_name = sender_name


class Slidestore(UserMixin, db.Model):
    __tablename__ = 'slidestore'
    slide_id = db.Column(db.Integer, primary_key=True)
    level = db.Column(db.Integer, nullable=False)
    course = db.Column(db.String(32), nullable=False)
    slide_type = db.Column(db.String(10), nullable=False)
    slide_name = db.Column(db.String(64), nullable=False)
    slide_path = db.Column(JSONB(), nullable=False)   
    publisher = db.Column(db.String(32), nullable=False)

    def __init__(self, level, course, slide_type, slide_path, slide_name, publisher):
        self.level = level
        self.course = course
        self.slide_type = slide_type
        self.slide_name = slide_name
        self.slide_path = slide_path
        self.publisher = publisher


class Help(UserMixin, db.Model):
    __tablename__ = 'help'
    help_id = db.Column(db.Integer, primary_key=True)
    help_topic = db.Column(db.String(60), nullable=False)
    help_content = db.Column(db.String(10000), nullable=False)

    def __init__(self, help_topic, help_content):
        self.help_topic = help_topic
        self.help_content = help_content


def connect_to_db(app):
    """Connect the database to our Flask app."""
    db.app = app
    db.init_app(app)
    db.create_all()


def build_db():
    db.drop_all()
    db.create_all()

    help_note = [
        {
            'help_topic': "Can't Login?",
            'help_content': "if you cant login please recover your account with a valid phone number or email."
        },
        {
            'help_topic': "Recover Password",
            'help_content': "At the login page ...click on forgot password.you willthen  be redirected to the forget page.where you can recover account with a verified phone number or email..A link will be send to you ..open it and  create your new password..remember the link only last for 10 minutes..if it expires ...please goto your profile and request for another"
        }
    ]

    for entry in help_note:
        help_topic = entry['help_topic']
        help_content = entry['help_content']
        new_help = Help(help_topic=help_topic, help_content=help_content)
        db.session.add(new_help)
        db.session.commit()
    
    
    admin_user = [
        {
            'username': "Otc Chingy",
            'password': "sha256$caEGaaX3$226063251f81d152c933b971cd25f4f16efb5a42f3a2f2bbbfc3b6db106ef988",
            'firstname': "Bernard",
            'lastname': "Azumah",
            'profile_pic': "/static/uploads/photos/Ben 20170502_095605.jpg",
            'phone': "233553567950",
            'email': "chingy.debillz@gmail.com",
            'confirmed_email': "true",
            'confirmed_phone': "true",
            'about': "My name is Bernard Azumah, C.E.O of TechUP Studio, you can call me Otc Chingy.",
            'gender': "male",
            'status': 1,
            'user_status': "goduser"
        }
    ]

    
    try:
        for entry in admin_user:
            new_user = Users(username=entry['username'], password=entry['password'], firstname=entry['firstname'],
                            lastname=entry['lastname'], email=entry['email'], phone=entry['phone'], about=entry['about'],
                            dateofbirth=datetime.date(year=1997, month=9, day=5), user_status=entry['user_status'])
            db.session.add(new_user)
            db.session.commit()
            print('Admin user created')
    except Exception:
        print('Admin user already created')
    user = Users.query.filter_by(username = (admin_user[0])['username']).first()
    if user:
        user.profile_pic = (admin_user[0])['profile_pic']
        user.status = (admin_user[0])['status']
        user.gender = (admin_user[0])['gender']
        db.session.add(user)
        db.session.commit()
        print('Admin user details added')

if __name__ == "__main__":
    from app import app

    connect_to_db(app)
    db.create_all()
    build_db()
    print("Connected to DB\nTables created\nConnection Available ")