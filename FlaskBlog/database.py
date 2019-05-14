import datetime
from sqlalchemy.dialects.postgresql import JSONB
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
# from app import getDate

db = SQLAlchemy()


class Admins(UserMixin, db.Model):
    __tablename__ = 'admins'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True)
    password = db.Column(db.String(120))
    firstname = db.Column(db.String(32))
    lastname = db.Column(db.String(32))
    profile_pic = db.Column(db.String(80), nullable=True)
    phone = db.Column(db.String(13), unique=True)
    email = db.Column(db.String(60), unique=True)
    adminkey = db.Column(db.String(120), unique=True)
    user_status = db.Column(db.String(10))

    def __init__(self, firstname, lastname, username, password, phone, email, user_status):
        self.firstname = firstname
        self.lastname = lastname
        self.username = username
        self.password = password
        self.phone = phone
        self.email = email
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


class Subscibers(UserMixin, db.Model):
    __tablename__ = 'subscribers'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String)
    verified = db.Column(db.Integer)

    def __init__(self, email):
        self.email = email



class Feedbacks(UserMixin, db.Model):
    __tablename__ = 'feedbacks'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), nullable=False)
    email = db.Column(db.String(60), nullable=True)
    phone = db.Column(db.String(13), unique=True)
    content =  db.Column(db.String(5000), nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.datetime.now())

    def __init__(self, name, email, phone, content, timestamp):
        self.name = name
        self.email = email
        self.phone = phone
        self.content = content
        self.timestamp = timestamp



class Posts(UserMixin, db.Model):
    __tablename__ = 'posts'
    post_id = db.Column(db.Integer, primary_key=True)
    post_content = db.Column(JSONB())
    privacy = db.Column(db.String(8), default='public')
    edited = db.Column(db.String(4), nullable=True)
    timestamp = db.Column(db.String(40))


    def __init__(self, post_content, privacy, timestamp):
        self.post_content = post_content
        self.privacy = privacy
        self.timestamp = timestamp


class Gallery(UserMixin, db.Model):
    __tablename__ = 'gallery'
    gallery_id = db.Column(db.Integer, primary_key=True)
    upload_type = db.Column(db.String(8))
    upload_used_as = db.Column(db.String(20))
    upload_path = db.Column(JSONB())
    privacy = db.Column(db.String(8), default='public')
    timestamp = db.Column(db.DateTime, default=datetime.datetime.now())

    def __init__(self, upload_type, upload_path, upload_used_as, privacy, timestamp):
        self.gallery_type = upload_type
        self.upload_type = upload_type
        self.upload_used_as = upload_used_as
        self.upload_path = upload_path
        self.privacy = privacy
        self.timestamp = timestamp


def connect_to_db(app):
    """Connect the database to our Flask app."""
    db.app = app
    db.init_app(app)
    db.create_all()


def build_db():
    db.drop_all()
    db.create_all()

    # help_note = [
    #     {
    #         'help_topic': "Can't Login?",
    #         'help_content': "if you cant login please recover your account with a valid phone number or email."
    #     },
    #     {
    #         'help_topic': "Recover Password",
    #         'help_content': "At the login page ...click on forgot password.you willthen  be redirected to the forget page.where you can recover account with a verified phone number or email..A link will be send to you ..open it and  create your new password..remember the link only last for 10 minutes..if it expires ...please goto your profile and request for another"
    #     }
    # ]

    # for entry in help_note:
    #     help_topic = entry['help_topic']
    #     help_content = entry['help_content']
    #     new_help = Help(help_topic=help_topic, help_content=help_content)
    #     db.session.add(new_help)
    #     db.session.commit()
    
    
    admin_user = [
        {
            'username': "Otc Chingy",
            'password': "sha256$caEGaaX3$226063251f81d152c933b971cd25f4f16efb5a42f3a2f2bbbfc3b6db106ef988",
            'firstname': "Bernard",
            'lastname': "Azumah",
            'profile_pic': "/static/uploads/photos/Ben 20170502_095605.jpg",
            'phone': "233553567950",
            'email': "chingy.debillz@gmail.com",
            'user_status': "goduser"
        }
    ]

    
    try:
        for entry in admin_user:
            new_user = Admins(username=entry['username'], password=entry['password'], firstname=entry['firstname'],
                            lastname=entry['lastname'], email=entry['email'], phone=entry['phone'],
                            user_status=entry['user_status'])
            db.session.add(new_user)
            db.session.commit()
            print('Admin user created')
    except Exception:
        print('Admin user already created')
    user = Admins.query.filter_by(username = (admin_user[0])['username']).first()
    if user:
        user.profile_pic = (admin_user[0])['profile_pic']
        db.session.add(user)
        db.session.commit()
        print('Admin user details added')

if __name__ == "__main__":
    from app import app

    connect_to_db(app)
    build_db()
    print("Connected to DB\nTables created\nConnection Available ")