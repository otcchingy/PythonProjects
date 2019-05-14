from flask_uploads import UploadSet, configure_uploads, extension, patch_request_class, IMAGES, AUDIO, DOCUMENTS
from itsdangerous import URLSafeTimedSerializer, URLSafeSerializer, SignatureExpired, BadSignature
from flask_login import LoginManager, login_required, logout_user, current_user
from flask import Flask, redirect, url_for, flash, g, jsonify, request, abort
from werkzeug.security import generate_password_hash, check_password_hash
from flask_socketio import SocketIO, emit, leave_room, join_room, send
from sqlalchemy.sql.expression import desc, and_, or_, func, cast
from flask_jwt import JWT, jwt_required, current_identity
from flask_admin.contrib.sqla.view import ModelView
from sqlalchemy.dialects.postgresql import JSONB
from flask_admin.base import expose, Admin
from flask_bootstrap import Bootstrap
from flask_mail import Mail, Message
from flask_admin.contrib import sqla
from flask_restful import Resource
from operator import attrgetter
from twilio_app import twilio_send
import flask_admin as admins
from flask_restful import Api
from database import *
import os

from twilio_app import twilio_send

app = Flask(__name__)
app.config['SECRET_KEY'] = "iamotc&ifuckingrule@#techup#"
# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://jfvhvyrisvbkzk:8134222a346acf6484020a4c07a805b0fa6e4f6ca97b3f51105a745b601f8027@ec2-107-21-98-165.compute-1.amazonaws.com:5432/d4s49sa8pb9hb'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:Asdwe111@localhost:5432/storylane'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config.from_pyfile('config.cfg')
Bootstrap(app)
mail = Mail(app)
socketio = SocketIO(app)
VIDEO = tuple('mp4 mkv flv gif mov ogv webm mpg avi'.split())
photos = UploadSet('photos', IMAGES)
audios = UploadSet('audios', AUDIO)
videos = UploadSet('videos', VIDEO)
slides = UploadSet('slides', DOCUMENTS)
documents = UploadSet('documents', DOCUMENTS)
app.config['UPLOADED_PHOTOS_DEST'] = os.getcwd() + '/static/uploads/photos'
app.config['UPLOADED_AUDIOS_DEST'] = os.getcwd() + '/static/uploads/audios'
app.config['UPLOADED_VIDEOS_DEST'] = os.getcwd() + '/static/uploads/videos'
app.config['UPLOADED_SLIDES_DEST'] = os.getcwd() + '/static/uploads/slides'
app.config['UPLOADED_DOCUMENTS_DEST'] = os.getcwd() + '/static/uploads/documents'
app.config['UPLOADED_AUDIOS_ALLOW'] = tuple('wma m4a mp2 au'.split())
app.config['UPLOADED_DOCUMENTS_ALLOW'] = tuple('pdf txt ppt pptx xlsx zip htm html tar rar gz py pyd exe cpp c'.split())
configure_uploads(app, (photos, audios, documents, videos))
patch_request_class(app)
s = URLSafeTimedSerializer(app.config['SECRET_KEY'])
x = URLSafeSerializer('keyupgaurdup')
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
api = Api(app)

# global vars
online_users = hang_users = chat_buddy = explore_seen = ago_list = {}


def authenticate(username, password):
    user = Users.query.filter_by(username=username).first()
    e_user = Users.query.filter_by(email=username).first()
    p_user = Users.query.filter_by(phone=username).first()
    if user:
        if check_password_hash(user.password, password):
            return user
    elif e_user:
        if check_password_hash(e_user.password, password):
            return e_user
    elif p_user:
        if check_password_hash(p_user.password, password):
            return p_user
    else:
        return None


def identity(payload):
    return Users.query.filter_by(id=payload['identity']).first()


jwt = JWT(app, authenticate, identity)


# ********MAIN ROUTES***********

@app.before_request
def before_request():
    g.user = current_user


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


# *******ADMIN ROUTE***********#

# Create customized model view class
class MyModelView(sqla.ModelView):
    def is_accessible(self):
        user = self.get_user()
        if current_user.is_authenticated:
            if user.user_status == 'goduser':
                return current_user.is_authenticated
            abort(404)
        return redirect(url_for('.login_view'))

    def get_user(self):
        return db.session.query(Users).filter_by(username=str(current_user)).first_or_404()


class UsersAdmin(ModelView):
    column_searchable_list = ('username', 'email', 'firstname', 'lastname', 'gender', 'status', 'user_status')
    column_filters = ('firstname', 'lastname', 'username', 'email', 'gender', 'status', 'user_status')


class HelpAdmin(ModelView):
    column_searchable_list = ('help_topic', 'help_content')
    column_filters = ('help_topic', 'help_content')


# Create customized index view class that handles login 
class MyAdminIndexView(admins.AdminIndexView):
    @expose('/')
    def index(self):
        user = self.get_user()
        if current_user.is_authenticated:
            if user.user_status == 'goduser':
                return super(MyAdminIndexView, self).index()
            abort(404)
        return redirect(url_for('.login_view'))

    def get_user(self):
        return db.session.query(Users).filter_by(username=str(current_user)).first_or_404()

    @expose('/logout/', methods=('GET', 'POST'))
    def logout_view(self):
        user = self.get_user()
        if current_user.is_authenticated:
            if user.user_status == 'goduser':
                logout_user()
                return redirect(url_for('logout'))
            abort(404)
        abort(404)


admin = Admin(app, 'ChatAPP', index_view=MyAdminIndexView(), base_template='my_master.html')

admin.add_view(UsersAdmin(Users, db.session))
admin.add_view(MyModelView(Friends, db.session))
admin.add_view(MyModelView(Follows, db.session))
admin.add_view(MyModelView(Storys, db.session))
admin.add_view(MyModelView(Notifications, db.session))
admin.add_view(HelpAdmin(Help, db.session))
admin.add_view(MyModelView(Gallery, db.session))
admin.add_view(MyModelView(Likes, db.session))
admin.add_view(MyModelView(Messages, db.session))
admin.add_view(MyModelView(Comments, db.session))
admin.add_view(MyModelView(Comment_likes, db.session))


# ****END OF ADMIN ROUTES*******#

##############################################################
##############################################################


def user_exists(username):
    user = get_user(username=username)
    if user:
        return True


def email_exists(email):
    email = get_user(email=email)
    if email:
        return True


def tel_exists(phone):
    tel = Users.query.filter_by(phone=phone).first()
    if tel:
        return True


def input_not_exist(data):
    email = get_user(email=data)
    phone = get_user(phone=data)
    try:
        if not email:
            if not phone:
                return True
    except Exception:
        return True


def invalid(data, password):
    user = get_user(username=data)
    e_user = get_user(email=data)
    p_user = get_user(phone=data)
    try:
        if not user or not check_password_hash(user.password, password):
            if not e_user or not check_password_hash(e_user.password, password):
                if not p_user or not check_password_hash(p_user.password, password):
                    return True
    except Exception:
        return True


# *******APP FUNCTIONS******#


def buildJson(tag: str, list_data: list):
    jsondata = {}
    for i in range(len(list_data)):
        name = str(tag) + str(i + 1)
        data = list_data[i]
        if not isinstance(list_data[i], str):
            data = data.toDict()
        jsondata[f"{name}"] = data
    return jsondata


def get_suggestions(friends=None, clubs=None, pages=None, apps=None, games=None):
    pass


def get_friend_requests_from_user(user):
    ofriends = Friends.query.filter(Friends.friend_id == user.id, Friends.pending == 'true').all()
    lists = []
    for results in ofriends:
        lists.append(results.user_id)
    return lists


def get_friend_requests_to_user(user):
    ufriends = Friends.query.filter(Friends.user_id == user.id, Friends.pending == 'true').all()
    lists = []
    for results in ufriends:
        lists.append(results.friend_id)
    return lists


def friends_id_list(user):
    ufriends = Friends.query.filter(Friends.user_id == user.id, Friends.pending == 'done').all()
    ofriends = Friends.query.filter(Friends.friend_id == user.id, Friends.pending == 'done').all()
    lists = []
    for result in ufriends:
        lists.append(result.friend_id)
    for results in ofriends:
        lists.append(results.user_id)
    return lists


def friends_checker(user, other_user):
    friends = friends_id_list(user)
    if type(other_user) != int:
        try:
            user_id = other_user.user_id
            if user_id in friends:
                return True
            else:
                return False
        except Exception:
            try:
                id_ = other_user.id
                if id_:
                    if id_ in friends:
                        return True
                    else:
                        return False
            except Exception:
                return 'failed'
    else:
        if other_user in friends:
            return True
        else:
            return False


def like(user, sectionid, comment=None):
    if comment:
        comment_ = Comments.query.filter_by(comment_id=sectionid).first()
        if comment_:
            check = check_if_liked(user, sectionid, comment=True)
            if check == False:
                new_like = Comment_likes(comment_id=sectionid, liker=user.id, timestamp=datetime.datetime.now())
                db.session.add(new_like)
                db.session.commit()
                return 'done'
            return 'failed'
        return 'failed'
    else:
        post = Storys.query.filter_by(story_id=sectionid).first()
        if post:
            check = check_if_liked(user, sectionid)
            if check == False:
                new_like = Likes(story_id=sectionid, liker=user.id, timestamp=datetime.datetime.now())
                db.session.add(new_like)
                db.session.commit()
                return 'done'
            return 'failed'
        return 'failed'


def unlike(user, sectionid, comment=None):
    if comment:
        comment_ = Comments.query.filter_by(comment_id=sectionid).first()
        if comment_:
            check = check_if_liked(user, sectionid, comment=True)
            if check == True:
                like = Comment_likes.query.filter(Comment_likes.comment_id == sectionid,
                                                  Comment_likes.liker == user.id).first()
                if like:
                    db.session.delete(like)
                    db.session.commit()
                    return 'done'
                return 'failed'
            return 'failed'
        return 'failed'
    else:
        post = Storys.query.filter_by(story_id=sectionid).first()
        if post:
            check = check_if_liked(user, sectionid)
            if check == True:
                like = Likes.query.filter(Likes.story_id == sectionid, Likes.liker == user.id).first()
                if like:
                    db.session.delete(like)
                    db.session.commit()
                    return 'done'
                return 'failed'
            return 'failed'
        return 'failed'


def comment(user, storyid, content):
    post = Storys.query.filter_by(story_id=storyid).first()
    if post:
        if content.isspace() == False and content != '':
            comment = Comments(user_id=user.id, post_id=storyid, comment_content=content,
                               timestamp=datetime.datetime.now())
            db.session.add(comment)
            db.session.commit()
            return 'done'
        return 'failed'
    return 'failed'


def check_if_liked(user, sectionid, comment=None):
    if comment:
        check = Comment_likes.query.filter(Comment_likes.liker == user.id,
                                           Comment_likes.comment_id == sectionid).first()
        if check:
            return True
        else:
            return False
    else:
        check = Likes.query.filter(Likes.liker == user.id, Likes.story_id == sectionid).first()
        if check:
            return True
        else:
            return False


def get_user(userid=None, username=None, email=None, phone=None, auth=None, noteid=None, storyid=None, messageid=None,
             commentid=None):
    if userid:
        if type(userid) == int:
            try:
                user = Users.query.filter_by(id=userid).first()
                if user:
                    return user
                else:
                    return None
            except Exception:
                return None
        else:
            return None
    elif username:
        try:
            user = Users.query.filter_by(username=username).first()
            return user
        except Exception:
            return None
    elif email:
        try:
            user = Users.query.filter_by(email=email).first()
            return user
        except Exception:
            return None
    elif phone:
        try:
            number = ('233{}'.format(phone[1:len(phone)]))
            user = Users.query.filter_by(phone=number).first()
            if user:
                return user
            else:
                return None
        except Exception:
            return None
    elif auth:
        try:
            user = Users.query.filter_by(auth_token=auth).first()
            if user:
                return user
            else:
                return None
        except Exception:
            return None
    elif noteid:
        if type(noteid) == int:
            try:
                check = Notifications.query.filter_by(note_id=noteid).first()
                if check:
                    user = Users.query.filter_by(id=check.user_id).first()
                    return user
                else:
                    return None
            except Exception:
                return None
        else:
            return None
    elif storyid:
        if type(storyid) == int:
            try:
                check = Storys.query.filter_by(story_id=storyid).first()
                if check:
                    user = Users.query.filter_by(id=check.user_id).first()
                    return user
                else:
                    return None
            except Exception:
                return None
        else:
            return None
    elif messageid:
        if type(messageid) == int:
            try:
                check = Messages.query.filter_by(message_id=messageid).first()
                if check:
                    user = Users.query.filter_by(id=check.sender_id).first()
                    return user
                else:
                    return None
            except Exception:
                return None
        else:
            return None
    elif commentid:
        if type(commentid) == int:
            try:
                check = Comments.query.filter_by(comment_id=commentid).first()
                if check:
                    user = Users.query.filter_by(id=check.user_id).first()
                    return user
                else:
                    return None
            except Exception:
                return None
        else:
            return None
    else:
        return None


def get_likes(sectionid, comment=None, count=None):
    if comment:
        likers = Comment_likes.query.filter(Comment_likes.comment_id == sectionid).all()
    else:
        likers = Likes.query.filter(Likes.story_id == sectionid).all()
    if count:
        count_likes = len(likers)
        return count_likes
    else:
        return likers


def get_comments(storyid, count=None):
    commenters = Comments.query.filter(Comments.story_id == storyid).all()
    if count:
        count_comments = Comments.query.filter(Comments.story_id == storyid).count()
        return count_comments
    else:
        if commenters:
            return commenters
        return 'failed'


def add_friend(user, friend):
    check = get_friendship(user, friend)
    if check is None and friend != user.id:
        addcode = '{}+{}'.format(user.id, friend)
        add_user = Friends(user_id=user.id, friend_id=friend, pending='true', add_code=addcode)
        notify = Notifications(user_id=user.id, sender_name=user.username, note_header='FRQ', note_receiver=friend,
                               note_content='would you be my friend?', timestamp=datetime.datetime.now())
        db.session.add(add_user)
        db.session.add(notify)
        db.session.commit()
        return 'done'
    return 'failed'


def get_stories(user, start, category=None):
    category = str(category)
    start = int(start)
    x = 0
    index = start
    stream = []
    streams = []
    ago = []
    lists = friends_id_list(user)
    if category == "self":
        limit = 5
        streamz = Storys.query.filter(Storys.user_id == user.id, Storys.privacy == 'public') \
            .order_by(desc('timestamp')).all()
    elif category == "explore":
        lists.append(user.id)
        try:
            seen = explore_seen[user.id]
        except KeyError:
            seen = []
        streams = Storys.query.filter(Storys.user_id.notin_(lists), Storys.story_id.notin_(seen)) \
            .order_by(func.random()).limit(5).all()
        if streams != []:
            for stream in streams:
                seen.append(stream.story_id)
            return streams
        return 'failed'
    else:
        stream += Storys.query.filter_by(user_id=user.id).all()
        for ids in lists:
            get_post = Storys.query.filter_by(user_id=ids).order_by(desc('timestamp')).limit(10).all()
            stream += get_post
        limit = 3
        streamz = sorted(stream, key=attrgetter('timestamp'), reverse=True)

    if streamz == []:
        return 'failed'
    else:
        while x != limit:
            try:
                post = streamz[index]
                streams.append(post)
                index += 1
                if index >= len(streamz):
                    for data in streams:
                        ago.append(data.story_id)
                    ago_list[user.id] = ago
                    streams.append('reachedMax')
                    return streams
                else:
                    x += 1
            except Exception as e:
                print(e)
                return 'failed'
        for data in streams:
            ago.append(data.story_id)
        ago_list[user.id] = ago
        return streams


def get_messages(user, friend, start):
    messages = Messages.query.filter(or_((and_(Messages.sender_id == user.id, Messages.receiver_id == friend)), (
        and_(Messages.sender_id == friend, Messages.receiver_id == user.id)))).order_by(desc('timestamp')).all()
    if messages:
        do_before(user, friend, action='get_messages')
        x = 0
        index = start
        previous_messages = []
        while x != 20:
            try:
                message = messages[index]
                previous_messages.append(message)
                index += 1
                if index >= len(messages):
                    previous_messages.append('reachedMax')
                    return previous_messages[::-1]
                    break
                else:
                    x += 1
            except Exception:
                return 'failed'
        return previous_messages[::-1]
    return 'failed'


def unfriend(user, userid):
    friendship = get_friendship(user, userid)
    if friendship:
        db.session.delete(friendship)
        db.session.commit()
        return 'done'
    return 'failed'


def accept(user, friend):
    person = get_user(userid=friend)
    if person:
        addcode = "{}+{}".format(friend, user.id)
        notify = Notifications(user_id=user.id, sender_name=user.username, note_header='AFR', note_receiver=friend,
                               note_content='{} accepted your friend request'.format(user.username),
                               timestamp=datetime.datetime.now())
        check_uff = check_if_following(user, friend)
        check_ffu = check_if_following(person, user.id)
        if not check_uff:
            follow_user = Follows(follower=friend, following=user.id, add_code=addcode)
            db.session.add(follow_user)
        if not check_ffu:
            follow_friend = Follows(follower=user.id, following=friend, add_code=addcode[::-1])
            db.session.add(follow_friend)
        new_friend = get_friendship(user, friend)
        if new_friend and new_friend.pending == 'true':
            new_friend.pending = 'done'
            db.session.add(new_friend)
            db.session.add(notify)
            db.session.commit()
            return 'done'
        return 'failed'
    return 'failed'


def decline(user, friend):
    request = get_friendship(user, friend)
    if request:
        db.session.delete(request)
        db.session.commit()
        return 'done'
    return 'failed'


def follow(user, friend):
    person = get_user(userid=friend)
    if person:
        check = check_if_following(user, friend)
        if not check:
            followcode = '{}+{}'.format(user.id, person.id)
            follow_friend = Follows(follower=user.id, following=person.id, add_code=followcode)
            notify = Notifications(user_id=user.id, sender_name=user.username, note_header='FLW',
                                   note_receiver=person.id, note_content='I jux Followed you?',
                                   timestamp=datetime.datetime.now())
            db.session.add(follow_friend)
            db.session.add(notify)
            db.session.commit()
            return 'done'
        return 'failed'
    return 'failed'


def unfollow(user, other_user):
    person = get_user(userid=other_user)
    if person:
        match = "{}+{}".format(user.id, person.id)
        unfollow_request = Follows.query.filter_by(add_code=match).first()
        if unfollow_request:
            db.session.delete(unfollow_request)
            db.session.commit()
            return 'done'
        return 'failed'
    return 'failed'


def get_followers(user, count=None):
    followers = Follows.query.filter(Follows.following == user.id).count()
    if count:
        return len(followers)
    return followers


def check_if_following(user, friend):
    person = get_user(userid=friend)
    try:
        if person:
            check = Follows.query.filter(Follows.follower == user.id, Follows.following == person.id).first()
            if check:
                return True
            return False
        return 'failed'
    except Exception:
        return 'failed'


def get_mutual_friends(user, friend, count=None):
    try:
        mutual_list = []
        mutualfriends = []
        ufriends = friends_id_list(user)
        ofriends = friends_id_list(friend)
        for id_ in ufriends:
            if id_ in ofriends:
                mutual_list.append(id_)
            else:
                continue
        if count:
            return len(mutual_list)
        else:
            for _id in mutual_list:
                mutual_user = get_user(userid=_id)
                if mutual_user:
                    mutualfriends.append(mutual_user)
                else:
                    continue
            return mutualfriends
    except Exception:
        return 'failed'


def get_friendship(user, friend):
    addcode = '{}+{}'.format(user.id, friend)
    friendship = Friends.query.filter(or_(Friends.add_code == addcode, Friends.add_code == addcode[::-1])).first()
    if friendship:
        return friendship
    else:
        return None


def upload(user, media, privacy='public', used_as='post'):
    try:
        paths = []
        audio = tuple('wma m4a mp2 au'.split())
        documents = tuple('pdf txt ppt pptx xlsx zip htm html tar rar gz py pyd js exe cpp c'.split())
        print(media)
        for file in media:
            print(file)
            print(file.mimetype)
            name = file.filename
            ext = extension(name)
            postname = name[:-(len(ext) + 1)]

            if used_as == 'slide':
                filetype = ext
                filename = slides.save(file, name='Slide.')
                path = "/static/uploads/slides/{}".format(filename)
                return {'status': 'done', 'ext': ext, 'filename': filename, 'path': path}
            elif ext.lower() in IMAGES:
                filetype = 'photo'
                filename = photos.save(file, name='Photo.')
                path = "/static/uploads/photos/{}".format(filename)
                paths.append(path)
            elif ext.lower() in AUDIO or ext.lower() in audio:
                filetype = 'audio'
                filename = audios.save(file, name='Audio.')
                path = "/static/uploads/audios/{}".format(filename)
                paths.append(path)
            elif ext.lower() in VIDEO:
                filetype = 'video'
                filename = videos.save(file, name='Video.')
                path = "/static/uploads/videos/{}".format(filename)
                paths.append(path)
            elif ext.lower() in documents or ext.lower() in documents:
                filetype = 'documents'
                filename = documents.save(file, name='Document.')
                path = "/static/uploads/documents/{}".format(filename)
                paths.append(path)
            else:
                pass
        print(paths)
        if len(paths) > 1:
            filetype = 'batch'
        else:
            filetype = filetype
            print(paths)
        print(filetype)
        new_upload = Gallery(user_id=user.id, upload_type=filetype, upload_used_as=used_as, upload_path=paths,
                             privacy=privacy, timestamp=datetime.datetime.now())
        db.session.add(new_upload)
        db.session.commit()
        if used_as == 'profile_pic':
            user.profile_pic = path
            db.session.add(user)
            db.session.commit()
            return {'status': 'done', 'path': paths, 'filetype': filetype, 'postname': postname}
        return {'status': 'done', 'path': paths, 'filetype': filetype, 'postname': postname}
    except Exception as e:
        print('error :' + str(e))
        return {'status': 'failed'}


def seen(noteid):
    seen_notice = Notifications.query.filter_by(note_id=noteid).first()
    if seen_notice and seen_notice.seen == None:
        seen_notice.seen = 'true'
        db.session.add(seen_notice)
        db.session.commit()
        return 'done'
    return 'failed'


def do_before(user, friend, noteid=None, action=None):
    if action == 'addfriend' or action == 'unfriend':
        if action == 'addfriend':
            check = get_friendship(user, friend)
            if not check:
                pass
            else:
                return 'ok'
        if action == 'unfriend':
            check = get_friendship(user, friend)
            if check:
                pass
            else:
                return 'ok'
        notes1 = Notifications.query.filter(Notifications.user_id == friend, Notifications.note_receiver == user.id, (
            or_(Notifications.note_header == 'FRQ', Notifications.note_header == 'AFR'))).all()
        notes2 = Notifications.query.filter(Notifications.user_id == user.id, Notifications.note_receiver == friend, (
            or_(Notifications.note_header == 'FRQ', Notifications.note_header == 'AFR'))).all()
        if notes1 or notes2:
            for note in (notes1 + notes2):
                db.session.delete(note)
            db.session.commit()
            return 'done'
        return 'ok'
    elif action == 'follow' or action == 'unfollow':
        notes = Notifications.query.filter(Notifications.user_id == user.id, Notifications.note_receiver == friend,
                                           Notifications.note_header == 'FLW').all()
        if notes:
            for note in notes:
                db.session.delete(note)
            db.session.commit()
            return 'done'
        return 'done'
    elif action == 'accept' or action == 'decline':
        notes = Notifications.query.filter(Notifications.user_id == user.id, Notifications.note_receiver == friend,
                                           Notifications.note_header == 'AFR').all()
        if notes:
            for note in notes:
                db.session.delete(note)
            db.session.commit()
            return 'done'
        return 'done'
    elif action == 'deletenote':
        note = Notifications.query.filter_by(note_id=noteid).first()
        if note.note_header == 'FRQ':
            request = get_friendship(user, note.user_id)
            notes1 = Notifications.query.filter(Notifications.user_id == note.note_receiver,
                                                Notifications.note_receiver == note.note_id,
                                                Notifications.note_header == 'AFR').all()
            notes1 = [] if notes1 == None else notes1
            if notes1:
                for note in notes1:
                    db.session.delete(note)
                db.session.commit()
            if request:
                db.session.delete(request)
                db.session.commit()
                return 'done'
            return 'done'
        return 'done'
    elif action == 'deleteafter':
        notes = Notifications.query.filter(Notifications.user_id == friend, Notifications.note_receiver == user.id,
                                           Notifications.note_header == 'FRQ').all()
        if notes:
            for note in notes:
                db.session.delete(note)
            db.session.commit()
            return 'done'
        return 'done'
    elif action == 'get_messages':
        messages = Messages.query.filter(Messages.sender_id == friend, Messages.receiver_id == user.id,
                                         Messages.seen == 0).all()
        if messages:
            for message in messages:
                message.seen = 1
                db.session.add(message)
            db.session.commit()
            return 'done'
        return 'failed'
    else:
        return 'failed'


def deleteIt(user, storyid=None, noteid=None, commentid=None, messageid=None, galleryid=None, path=None):
    if storyid:
        post = Storys.query.filter_by(story_id=storyid).first()
        likes = Likes.query.filter_by(story_id=storyid).all()
        comments = Comments.query.filter_by(story_id=storyid).all()
        if post:
            if post.user_id == user.id:
                if likes:
                    for result in likes:
                        db.session.delete(result)
                if comments:
                    for result in comments:
                        deleteIt(user, commentid=result.comment_id)
                if (post.story_content['media'][0])['filetype'] != 'None':
                    for media in post.story_content['media']:
                        file = Gallery.query.filter(Gallery.user_id == user.id, Gallery.upload_used_as == 'post',
                                                    Gallery.upload_path == cast((media['path']), JSONB)).first()
                        if file:
                            deleteIt(user, galleryid=file.gallery_id)
                db.session.delete(post)
                db.session.commit()
                return 'done'
            return 'failed'
        return 'failed'
    elif noteid:
        note = Notifications.query.filter_by(note_id=noteid).first()
        if note:
            db.session.delete(note)
            db.session.commit()
            return 'done'
        return 'failed'
    elif commentid:
        comment = Comments.query.filter_by(comment_id=commentid).first()
        person = get_user(storyid=comment.post_id)
        if comment:
            if comment.user_id == user.id or user.id == person.id:
                clikes = Comment_likes.query.filter_by(comment_id=commentid).all()
                for like in clikes:
                    db.session.delete(like)
                db.session.delete(comment)
                db.session.commit()
                return 'done'
            return 'failed'
        return 'failed'
    elif messageid:
        message = Messages.query.filter_by(message_id=messageid).first()
        if message:
            if message.sender == user.id:
                db.session.delete(message)
                db.session.commit()
                return 'done'
            return 'failed'
        return 'failed'
    elif galleryid:
        gallery_item = Gallery.query.filter_by(gallery_id=galleryid).first()
        if gallery_item:
            if gallery_item.user_id == user.id:
                deleteIt(user, path=gallery_item.upload_path)
                db.session.delete(gallery_item)
                db.session.commit()
                return 'done'
            return 'failed'
        return 'failed'
    elif path:
        for file in path:
            try:
                print("deleting file at" + file)
                file_path = os.getcwd() + file
                os.remove(file_path)
                print('deleted')
            except Exception:
                continue
        return 'done'
    else:
        return 'failed'


def time_past(dt):
    y = dt[:4]
    year = int(y)
    m = dt[5:7]
    month = int(m)
    d = dt[8:10]
    day = int(d)
    h = dt[11:13]
    hour = int(h)
    mn = dt[14:16]
    minute = int(mn)
    s = dt[17:19]
    second = int(s)
    ms = dt[20:26]
    microsecond = int(ms)
    period = datetime.datetime.now() - datetime.datetime(year, month, day, hour, minute, second, microsecond)
    return period


def time_ago(calc):
    dt = str(calc)
    t = time_past(dt)
    length = len(str(t))
    hour1 = (str(t))[:1]
    hour2 = (str(t))[:2]
    minutes = (str(t))[2:4]
    if t.days < 0:
        return 'just now'
    elif t.days > 0:
        if t.days == 1:
            return "{} day ago".format(t.days)
        return "{} days ago".format(t.days)
    elif length == 15:
        return hour2 + ' hours ago'
    elif length == 14:
        if hour1 != '0':
            if hour1 == '1':
                return hour1 + ' hour ago'
            return hour1 + ' hours ago'
        else:
            if int(minutes) == 0:
                return 'just now'
            elif int(minutes) == 1:
                return '1 minute ago'
            return '{} minutes ago'.format(int(minutes))
    else:
        return 'some time ago'


def get_games(user, get=None):
    pass


def get_gallery(user, get='all'):
    if get == 'all':
        all_gallery = Gallery.query.filter(Gallery.user_id == user.id).order_by(desc(Gallery.timestamp)).all()
        return all_gallery
    elif get == 'pics':
        pics_gallery = Gallery.query.filter(Gallery.user_id == user.id, (
            or_(Gallery.upload_type == 'photo', Gallery.upload_type == 'photo'))).order_by(
            desc(Gallery.timestamp)).all()
        return pics_gallery
    elif get == 'auds':
        pics_gallery = Gallery.query.filter(Gallery.user_id == user.id, Gallery.upload_type == 'audio').order_by(
            desc(Gallery.timestamp)).all()
        return pics_gallery
    elif get == 'vids':
        vids_gallery = Gallery.query.filter(Gallery.user_id == user.id, Gallery.upload_type == 'video').order_by(
            desc(Gallery.timestamp)).all()
        return vids_gallery
    elif get == 'docs':
        vids_gallery = Gallery.query.filter(Gallery.user_id == user.id, Gallery.upload_type == 'documents').order_by(
            desc(Gallery.timestamp)).all()
        return vids_gallery
    else:
        return 'failed'


def get_online_friends(user, online_users=online_users):
    online_friends = []
    friends = friends_id_list(user)
    for key in online_users:
        if key in friends:
            online_friends.append(key)
        else:
            continue
    return online_friends


def countit(nc=None, pc=None, mc=None):
    user = get_user(userid=1)
    if nc:
        notices = Notifications.query.filter(Notifications.note_receiver == user.id, Notifications.seen == None).count()
        return notices
    elif pc:
        # new_post = Posts.query.filter(user_id=user.id).order_by(desc(Posts.timestamp)).count()
        pass
    elif mc:
        count = 0
        messages = Unread_Messages.query.filter_by(receiver_id=user.id).all()
        for message in messages:
            count += message.count
        return count
    else:
        return 'failed'


def unread_messages(sender, friend, action=None):
    user = sender
    if action == 'add':
        if friends_checker(user, friend):
            check = Unread_Messages.query.filter(Unread_Messages.sender_id == user.id,
                                                 Unread_Messages.receiver_id == friend).first()
            if check:
                check.count = check.count + 1
                db.session.add(check)
                db.session.commit()
                return 'done'
            else:
                new_unread_messages = Unread_Messages(sender_id=user.id, receiver_id=friend, count=1)
                db.session.add(new_unread_messages)
                db.session.commit()
                return 'done'
        else:
            return 'failed'
    elif action == 'get':
        check = Unread_Messages.query.filter(Unread_Messages.sender_id == friend,
                                             Unread_Messages.receiver_id == user.id).first()
        try:
            if check != None:
                if check.count > 0:
                    return check.count
        except Exception:
            pass
    elif action == 'reset':
        reset = Unread_Messages.query.filter(Unread_Messages.sender_id == user.id,
                                             Unread_Messages.receiver_id == friend).first()
        if reset:
            reset.count = 0
            db.session.add(reset)
            db.session.commit()
            return 'done'
    else:
        return 'error'


def post(user, story, files):
    src = [{'filetype': 'None', 'path': 'None'}]
    if 'media' in files:  # request.files
        media = files.getlist('media')
        process = upload(user, media, privacy=story['privacy'], used_as='post')
        if process['status'] == 'done':
            path = process['path']
            type_ = process['filetype']
            postname = process['postname']
            src = [{'path': path, 'filetype': type_, 'filename': postname}]

    new_post = Storys(user_id=user.id, story_content={
        'title': story['title'], 'description': story['description'],
        'content': story['content'], 'media': src},
                      privacy=story['privacy'], timestamp=datetime.datetime.now())

    db.session.add(new_post)
    db.session.commit()
    flash("Post successfull!", "success")
    return 'done'


def edit_post(user, story, files):
    old_post = Storys.query.filter_by(story_id=story['storyid']).first()
    if user.id == old_post.user_id:
        edit = old_post
        if edit:
            post_media = (edit.story_content)['media']  # check if new media then change details for media else pass
            privacy = story['privacy']
            if 'media' in files:
                media = files.getlist('media')
                old_media = Gallery.query.filter(Gallery.user_id == user.id, Gallery.upload_used_as == 'post',
                                                 Gallery.upload_path == cast(
                                                     ((((edit.story_content)['media'])[0])['path']), JSONB)).first()
                deleteIt(user, galleryid=old_media.gallery_id)
                process = upload(user, media, privacy=story['privacy'], used_as='post')
                if process['status'] == 'done':
                    path = process['path']
                    type_ = process['filetype']
                    postname = process['postname']
                    post_media = [{'path': path, 'filetype': type_, 'filename': postname}]
                pass

            edit.story_content = {'title': story['title'], 'description': story['description'],
                                  'content': story['content'], 'media': post_media}
            edit.privacy = story['privacy']
            edit.timestamp = datetime.datetime.now()
            edit.edited = 'true'
            db.session.add(edit)
            db.session.commit()
        flash("The post has been succesfully updated", 'success')
        return 'done'
    flash("you don't have permission to edit this!!!", 'error')
    return 'failed'


def view_mutual_friends(user, friendid):
    friend = get_user(userid=friendid)
    if friend:
        mutual_friends = get_mutual_friends(user, friend)
    return redirect(url_for('friends'))


def view_profile(user, userid, username):
    visitor = get_user(userid=int(userid))
    if user.id != visitor.id:
        posted = Storys.query.filter(Storys.user_id == user.id, Storys.privacy == 'public').limit(3).all()
    return redirect(url_for('profile', username=visitor.username))


def change_password(user, old_password, new_password):
    password = user.password
    if check_password_hash(password, old_password):
        user.password = generate_password_hash(new_password, method='sha256')
        db.session.add(user)
        db.session.commit()
        flash("Your password has been succesfully updated", 'success')
        return jsonify({'status': 'done'})
    flash("password's don't match", 'error')
    return jsonify({'status': 'failed'})


def recover_we(user_email):
    if request.method == 'POST':
        user = get_user(email=user_email)
        if user:
            if user.confirmed_email == 'true':
                email = user_email
                token = s.dumps(email, salt='forgot.recovery@key')
                msg = Message('Password Reset', sender='chatapp.gh@gamil.com', recipients=[email])
                link = (url_for('reset', token=token, _external=True))
                msg.body = "Click the link {} to reset your password".format(link)
                msg.html = link
                mail.send(msg)
                flash('Email Sent, check your inbox and follow the steps', 'success')
                return redirect(url_for('login'))
            flash("Your email is not confirmed, please confirm to continue", 'error')
            return redirect(url_for('verify'))
        flash('Email not recognized', 'error')
        return redirect(url_for('recover_we'))
    flash('Validation Email not recognized', 'error')
    return redirect(url_for('recover_we'))


def recover_wp(user_phone):
    if request.method == 'POST':
        user = get_user(phone=user_phone)
        if user:
            if user.confirmed_phone == 'true':
                phone = user_phone
                token = s.dumps(phone, salt='forgot.recovery@key')
                link = (url_for('reset', token=token, _external=True))
                msg = (
                    "ChatAPP\n\n Reset Password \nClick the link\n {} \n to reset your password\n\nSender : Chingy@Chatapp.gh".format(
                        link))
                twilio_send(phone, msg)
                flash('Message Sent, check your inbox and follow the steps', 'success')
                return redirect(url_for('login'))
            flash("your phone number is not confirmed, please confirm to continue", 'error')
            return redirect(url_for('verify'))
        flash('phone number not recognized', 'error')
        return redirect(url_for('recover_wp'))
    flash('phone number not recognized', 'error')
    return redirect(url_for('recover_wp'))


def reset(token, new_password):
    try:
        data = s.loads(token, salt='forgot.recovery@key', max_age=600)
    except Exception:
        flash("You can't access this page, Invalid token!", 'error')
        return redirect(url_for('recover_we'))

    e_user = get_user(email=data)
    p_user = get_user(phone=data)
    if e_user or p_user:
        if request.method == 'POST':
            try:
                if e_user:
                    e_user.password = generate_password_hash(new_password, method='sha256')
                    db.session.add(e_user)
                    db.session.commit()
                    flash('Password changed successfully', 'success')
                    return redirect(url_for('login'))
                p_user.password = generate_password_hash(new_password, method='sha256')
                db.session.add(p_user)
                db.session.commit()
                flash('Password changed successfully', 'success')
                return redirect(url_for('login'))
            except Exception:
                if SignatureExpired:
                    flash("The link has expired, go to your profile and request for a new confirmation link", 'error')
                    return redirect(url_for('recover_we'))
                elif BadSignature:
                    flash("The link is invalid, please go to your profile and request for a confirmation link", 'error')
                    return redirect(url_for('settings'))
                else:
                    flash("Cannot recognize link, please login and request for an conformation link", 'error')
                    return redirect(url_for('recover_we'))
            return jsonify({'status': 'done'})
        return jsonify({'status': 'done'})
    flash("you can't access this page, invalid token!", 'error')
    return redirect(url_for('recover_we'))


def _help(help_search):
    if str(help_search).isspace() or help_search is None:
        return jsonify({'status': 'done'})
    help_results = Help.query.filter(
        or_(Help.help_topic.like("%{}%".format(help_search)), Help.help_content.like("%{}%".format(help_search)))).all()
    return jsonify({'status': 'done'})


def add_help(user, helptopic, helpcontent):
    if user.user_status == 'goduser':
        new_help_note = Help(help_topic=helptopic, help_content=helpcontent)
        db.session.add(new_help_note)
        db.session.commit()
        return redirect(url_for('_help'))


def verify(data):
    if '@' in data:
        user = get_user(email=data)
        if user:
            if user.confirmed_email != 'true':
                return redirect(url_for('send_confirmation_email', email=data, _external=True))
            flash('User already verified', 'error')
            return redirect(url_for('profile', username=user.username))
        flash('User does not exist, please register', 'error')
        return redirect(url_for('verify'))
    else:
        user = get_user(phone=data)
        if user:
            if user.confirmed_phone != 'true':
                return redirect(url_for('send_confirmation_link', phone=data, _external=True))
            flash('User already verified', 'error')
            return redirect(url_for('profile', username=user.username))
        flash('User does not exist, please register', 'error')
        return redirect(url_for('verify'))


def send_welcome_message(email):
    msg = Message('Welcome to ChatAPP', sender='chatapp@techupstudio.com', recipients=[email])
    msg.body = "Welcome to Chatapp, The best social network for Universities an colleges, Learn, share and have fun. "
    msg.html = ''
    mail.send(msg)


def send_confirmation_email(email):
    user = get_user(email=email)
    if user:
        if user.confirmed_email != 'true':
            token = s.dumps(email, salt='confirm-ekey')
            msg = Message('Ccfirm Email', sender='chatapp@techupstudio.com', recipients=[email])
            link = url_for('confirm_email', token=token, _external=True)
            msg.body = "Click the link {} to confirm your account".format(link)
            msg.html = link
            mail.send(msg)
            return redirect(url_for('login'))
        flash('User already verified', 'error')
        return redirect(url_for('profile', username=user.username))
    flash('Email not registered!', 'error')
    return redirect(url_for('verify'))


def send_confirmation_link(phone):
    user = get_user(phone=phone)
    if user:
        if user.confirmed_phone != 'true':
            token = s.dumps(phone, salt='confirm-pkey')
            link = url_for('confirm_phone', token=token, _external=True)
            msg = (
                "ChatAPP\n\n Confirm Number \nClick the link\n {} \n to confirm your account\n\nSender : Chingy@Chatapp.gh".format(
                    link))
            twilio_send(phone, msg)
            return redirect(url_for('login'))
        flash('User already verified', 'error')
        return redirect(url_for('profile', username=user.username))
    flash('Number not registered!', 'error')
    return redirect(url_for('verify'))


def confirm_email(token):
    try:
        if request.method == 'GET':
            email = s.loads(token, salt='confirm-ekey', max_age=1800)
            user = get_user(email=email)
            if user:
                if user.confirmed_email != 'true':
                    user.confirmed_email = 'true'
                    db.session.add(user)
                    db.session.commit()
                    return redirect(url_for('timeline'))
                flash('User already verified', 'error')
                return redirect(url_for('profile', username=user.username))
            flash('User does not exist!', 'error')
            return redirect(url_for('verify'))
        abort(404)
    except Exception:
        if SignatureExpired:
            flash(
                "Sorry '{}', The confimation link has expired, go to your profile and request for a new confirmation link".format(
                    user.username), 'error')
            return redirect(url_for('verify'))
        elif BadSignature:
            flash("The link is invalid, please go to your profile and request for a confirmation link", 'error')
            return redirect(url_for('settings'))
        else:
            flash("Cannot recognize link, please login and request for an conformation link", 'error')
            return redirect(url_for('verify'))


def confirm_phone(token):
    try:
        phone = s.loads(token, salt='confirm-pkey', max_age=1800)
        user = get_user(phone=phone)
        if user:
            if user.confirmed_email != 'true':
                user.confirmed_email = 'true'
                db.session.add(user)
                db.session.commit()
                return redirect(url_for('timeline'))
            flash('User already verified', 'error')
            return redirect(url_for('profile', username=user.username))
        flash('User does not exist!', 'error')
        return redirect(url_for('profile', username=user.username))
    except Exception:
        if SignatureExpired:
            flash("The confimation link has expired, go to your profile and request for a new confirmation link",
                  'error')
            return redirect(url_for('verify'))
        elif BadSignature:
            flash("The link is invalid, please go to your profile and request for a confirmation link", 'error')
            return redirect(url_for('settings'))
        else:
            flash("Cannot recognize link, please login and request for an conformation link", 'error')
            return redirect(url_for('verify'))


def processor(user, received):
    print("JSON to process = ", received)
    if received:
        action = received['action']
        try:  # friend/searchinteract
            friend = get_user(username=received['friend']).id
        except Exception:
            try:  # postsinteract
                storyid = int(received['storyid'])
            except Exception:
                try:  # noticeinteract
                    search = int(received['search'])
                except Exception:
                    try:  # check--seen--delete
                        note = int(received['note'])
                    except Exception:  # infinityscroll
                        try:
                            start = int(received['start'])
                            friend = received['friend']
                        except Exception:  # timeline
                            try:
                                storyid = int(received['storyid'])
                                content = received['comment']
                            except Exception:
                                try:
                                    storyid = int(received['storyid'])
                                except Exception:
                                    try:
                                        start = int(received['start'])
                                        friend = get_user(username=received['friend']).id
                                    except Exception:
                                        try:
                                            start = int(received['start'])
                                        except Exception:
                                            try:
                                                friend = get_user(username=received['friend']).id
                                            except Exception:
                                                media = received['media']
        if action == 'addfriend':
            do_before(user, friend=friend, action='addfriend')
            process = add_friend(user, friend)
            if process == 'done':
                return jsonify({'status': 'friendrequestsent', 'friend': friend})
            else:
                return jsonify({'status': 'failed'})
        elif action == 'unfriend' or action == 'friendrequestsent':
            do_before(user, friend=friend, action='unfriend')
            process = unfriend(user, friend)
            if process == 'done':
                return jsonify({'status': 'unfriended', 'friend': friend})
            else:
                return jsonify({'status': 'failed'})
        elif action == 'accept':
            do_before(user, friend=friend, action='accept')
            process = accept(user, friend)
            do_before(user, friend=friend, action='deleteafter')
            if process == 'done':
                return jsonify({'status': 'accepted'})
            else:
                return jsonify({'status': 'failed'})
        elif action == 'decline':
            do_before(user, friend=friend, action='decline')
            process = decline(user, friend)
            do_before(user, friend=friend, action='deleteafter')
            if process == 'done':
                return jsonify({'status': 'declined'})
            else:
                return jsonify({'status': 'failed'})
        elif action == 'follow':
            do_before(user, friend=friend, action='follow')
            process = follow(user, friend)
            if process == 'done':
                return jsonify({'status': 'followed', 'friend': friend})
            else:
                return jsonify({'status': 'failed'})
        elif action == 'unfollow':
            do_before(user, friend=friend, action='unfollow')
            process = unfollow(user, friend)
            if process == 'done':
                return jsonify({'status': 'unfollowed', 'friend': friend})
            else:
                return jsonify({'status': 'failed'})
        elif action == 'like':
            process = like(user, storyid)
            count = get_likes(storyid, count=True)
            if process == 'done':
                return jsonify({'status': 'liked', 'current_likes_count': count, 'storyid': storyid})
            else:
                return jsonify({'status': 'failed'})
        elif action == 'unlike':
            process = unlike(user, storyid)
            count = get_likes(storyid, count=True)
            if process == 'done':
                return jsonify({'status': 'unliked', 'current_likes_count': count, 'storyid': storyid})
            else:
                return jsonify({'status': 'failed'})
        elif action == 'delete':
            process = deleteIt(user, storyid=storyid)
            if process == 'done':
                return jsonify({'status': 'deleted'})
            else:
                return jsonify({'status': 'failed'})
        elif action == 'c_like':
            process = like(user, storyid, comment=True)
            count = get_likes(storyid, count=True, comment=True)
            if process == 'done':
                return jsonify({'status': 'c_liked', 'countlikes': count, 'storyid': storyid})
            else:
                return jsonify({'status': 'failed'})
        elif action == 'c_unlike':
            process = unlike(user, storyid, comment=True)
            count = get_likes(storyid, count=True, comment=True)
            if process == 'done':
                return jsonify({'status': 'c_unliked', 'countlikes': count, 'storyid': storyid})
            else:
                return jsonify({'status': 'failed'})
        elif action == 'c_delete':
            process = deleteIt(user, commentid=storyid)
            if process == 'done':
                return jsonify({'status': 'deleted'})
            else:
                return jsonify({'status': 'failed'})
        elif action == 'deletenote':
            do_before(user, friend=None, noteid=note, action='deletenote')
            process = deleteIt(user, noteid=note)
            if process == 'done':
                return jsonify({'status': 'deleted'})
            else:
                return jsonify({'status': 'failed'})
        elif action == 'seen':
            process = seen(noteid=note)
            if process == 'done':
                return jsonify({'status': 'seen', 'note': note})
            else:
                return jsonify({'status': 'failed'})
        elif action == 'previous_messages':
            process = get_messages(user, friend, start)
            if process != 'failed':
                return jsonify({'status': ''})
            else:
                return jsonify({'status': 'failed'})
        elif action == 'getcomments':
            process = get_comments(storyid=storyid)
            if process != 'failed':
                return jsonify({'status': 'done', 'storyid': storyid, 'count': get_comments(int(storyid), count=True)})
            else:
                return jsonify({'status': 'failed', 'storyid': storyid})
        elif action == 'postcomments':
            process = comment(user, storyid, content)
            if process != 'failed':
                return jsonify({'status': content, 'storyid': str(storyid), 'username': user.username})
            else:
                return jsonify({'status': 'failed'})
        elif action == 'loadmorepost':
            process = get_stories(user, start)
            if process == 'failed':
                return jsonify({'status': 'failed'})
            else:
                return jsonify(buildJson("Story", process))
        elif action == 'loadgallery':
            process = get_gallery(user, get=media)
            if process == 'failed':
                return jsonify({'status': 'failed'})
            else:
                return jsonify({'status': ''})
        elif action == 'explorestories':
            process = get_stories(user, start, category="explore")
            if process == 'failed':
                return jsonify({'status': 'failed'})
            else:
                return jsonify(buildJson("Story", process))
        elif action == 'loaduserpost':
            if friend == 'None':
                person = user
            else:
                person = get_user(username=friend)
            process = get_stories(person, start, category="self")
            if process == 'failed':
                return jsonify({'status': 'failed'})
            else:
                return jsonify(buildJson("Story", process))
        else:
            return jsonify({'status': 'failed'})
    return jsonify({'status': 'failed'})


##############################################################
##############################################################


@app.route('/')
def home():
    return jsonify({'status': 'connected'})


@app.errorhandler(404)
def lost(e):
    return jsonify({'status': 'error', 'code': '404'}), 404


@app.errorhandler(403)
def forbidden(e):
    return jsonify({'status': 'error', 'code': '403'}), 403


@app.errorhandler(400)
def bad_request(e):
    return jsonify({'status': 'error', 'code': '400'}), 400


@app.errorhandler(405)
def restricted(e):
    return jsonify({'status': 'error', 'code': '405'}), 405


@app.errorhandler(500)
def unavailable(e):
    return jsonify({'status': 'error', 'code': '500'}), 500


####################################################################
####################################################################
# SOCKECT IO SERVER (NOTIFICATION AND CHAT)
####################################################################

@socketio.on('connected')
@login_required
def user_connected():
    user = current_user
    online_users[user.id] = request.sid
    response = {'username': user.username, 'userid': user.id}
    friends = get_online_friends(user)
    if friends:
        for friend in friends:
            recipient_sid = online_users[friend]
            emit('friend_online', response, room=recipient_sid)


@socketio.on('disconnected')
@login_required
def user_disconnected():
    pass
    # user = current_user
    # try:
    #     print(request.sid)
    #     hang_users.__delitem__(user.id)
    #     online_users.__delitem__(user.id)
    # except Exception:
    #     print("disconnected")


@socketio.on('augMessage', namespace='/public')
@login_required
def handle_aug_message(msg):
    user = current_user
    sid = request.sid
    online_users[user.id] = sid
    room = 'allusersgroupmessage'
    if msg.lower() == '@commands':
        response = {'username': 'Commands',
                    'message': '@clear -- clear screen '
                               '<br/> @users -- count online hangers '
                               '<br/> @leave -- leave group '
                               '<br/> @friends -- show friends in group '
                               '<br/> @bot -- automate features [log old messages for you etc]'}
        emit('newaugMessage', response, room=sid)
    elif msg.lower() == '@users':
        response = {'username': 'Online Users', 'message': len(online_users)}
        emit('newaugMessage', response, room=sid)
    elif msg.lower() == '@bot':
        response = {'username': 'Hang Bot', 'message': 'bot is offline at the momment'}
        emit('newaugMessage', response, room=sid)
    elif msg.lower() == '@friends':
        response = {'username': 'Friends', 'message': '//get online friends in list and join with newline'}
        emit('newaugMessage', response, room=sid)
    elif msg.lower() == '@leave':
        leave_room(room, sid)
        response = {'username': user.username, 'message': 'left the room'}
        emit('newaugMessage', response, room=room)
    elif msg.isspace() == False and msg != '':
        response = {'username': user.username, 'message': msg}
        emit('newaugMessage', response, room=room, include_self=False)
    else:
        response = {'username': 'Failed!!!', 'message': 'something went wrong'}
        emit('newaugMessage', response, room=request.sid)


@socketio.on('hangroom', namespace='/public')
@login_required
def join_hangroom():
    user = current_user
    room = 'allusersgroupmessage'
    sid = request.sid
    online_users[user.id] = sid
    chat_buddy[user.id] = 0
    join_room(room, sid=sid)
    response = {'username': user.username, 'message': "What's Hanging?"}
    emit('newaugMessage', response, room=room, include_self=False)


@socketio.on('private_message', namespace='/private')
@login_required
def handle_private_message(data):
    user = current_user
    online_users[user.id] = request.sid
    recipient_id = int(data['userid'])
    buddy = get_user(userid=recipient_id)
    message = data['message']
    print(message)
    try:
        recipient_sid = online_users[recipient_id]
    except Exception:
        pass
    if message != '' and message.isspace() != True:
        new_message = Messages(sender_id=user.id, receiver_id=recipient_id, message_content=message,
                               timestamp=datetime.datetime.now())
        db.session.add(new_message)
        db.session.commit()
        response = {'username': user.username, 'message': message}
        if recipient_sid:
            emit('new_p_message', response, room=recipient_sid)

        try:
            if chat_buddy[recipient_id] != user.id:
                unread_messages(user, recipient_id, action='add')
            else:
                msg = Messages.query.filter_by(message_content=message).order_by(desc('timestamp')).first()
                msg.seen = 1
                db.session.add(msg)
                db.session.commit()
        except Exception:
            unread_messages(user, recipient_id, action='add')
        if recipient_sid:
            count = unread_messages(buddy, user.id, action='get')
            response = {'sender': 'unread{}'.format(user.id), 'count': count}
            emit('new_unread', response, room=recipient_sid)


@socketio.on('online_user', namespace='/private')
@login_required
def online_user():
    user = current_user
    online_friends = get_online_friends(user)
    if online_friends:
        emit('online_friends', online_friends)


@socketio.on('current_chat_buddy', namespace='/private')
@login_required
def current_chat_buddy(data):
    user = current_user
    friend = int(data)
    chat_buddy[user.id] = friend
    buddy = get_user(userid=friend)
    unread = unread_messages(user, friend, action='get')
    if unread is not None and unread > 0:
        unread_messages(buddy, user.id, action='reset')
        emit('reset_unread', 'unread{}'.format(friend), room=request.sid)


@socketio.on('join', namespace='/group')
@login_required
def on_join(data):
    user = current_user
    room = data['room']
    join_room(room)
    send(user.username + ' just joined.', room=room)


@socketio.on('leave', namespace='/group')
@login_required
def on_leave(data):
    user = current_user
    room = data['room']
    leave_room(room)
    send(user.username + ' has left.', room=room)


@socketio.on('message', namespace='/group')
@login_required
def receive_message(msg):
    pass
    # user = current_user
    # if is_banned(user.id):
    #     disconnect()
    # else:
    #     #send(msg, room=room)
    #     pass


@socketio.on('notify', namespace='/notification')
@login_required
def notify():
    unseen = countit(nc=True)
    unread = countit(mc=True)
    response = {'unseen': unseen, 'unread': unread}
    emit('notice', response)


@socketio.on('posts_time', namespace='/notification')
@login_required
def posts_time():
    user = current_user
    response = []
    try:
        posts_lists = ago_list[user.id]
        if posts_lists:
            for id_ in posts_lists:
                post = Storys.query.filter_by(story_id=id_).first()
                if post:
                    time_used = time_ago(post.timestamp)
                    response.append({'section': 'ago{}'.format(id_), 'time': time_used})
            emit('time_spent', response)
    except Exception:
        pass


@socketio.on_error_default
def default_error_handler(e):
    print(request.event["message"])  # "my error event"
    print(request.event["args"])  # (data)
    print(e)


class Test(Resource):

    @jwt_required()
    def get(self):
        print(request.json)
        print(request.form)
        print(request.files)
        print(current_identity.toDict())
        return jsonify(current_identity.toDict())

    def post(self):
        print(request.json)
        print(request.form)
        print(request.files)
        return jsonify({'status': 'done'})

    def put(self):
        pass

    def delete(self):
        pass


class UserManager(Resource):

    def get(self, username, detail=None):
        # detail = friends, followers, chats with user, gallery, stories, comments, likes etc
        return jsonify(get_user(username=username).toDict())

    def post(self):
        pass

    def put(self, username, field, value):
        pass

    def delete(self, username):
        pass


class Authenticate(Resource):

    @jwt_required()
    def get(self):
        return jsonify(current_identity.toDict())

    @jwt_required()
    def post(self):
        return jsonify(current_identity.toDict())


class ActivitySignup(Resource):

    def post(self, firstname, lastname, email, username, password):
        if user_exists(username):
            return jsonify({'status': 'failed', 'result': 'username already used!'})
        elif email_exists(email):
            return jsonify({'status': 'failed', 'result': 'email already used!'})
        else:
            hashpass = generate_password_hash(password, method='sha256')
            lastname = "" if lastname == "None" else lastname
            intro_about = 'My name is ' + firstname + ' ' + lastname + '. but you can call me ' + username + '.'
            new_user = Users(username=username, password=hashpass, firstname=firstname, lastname=lastname,
                             dateofbirth=None, email=email, about=intro_about, user_status='normal')
            db.session.add(new_user)
            db.session.commit()
            # email = form.email.data
            # phone = form.phone.data
            # redirect(url_for('send_confirmation_email', email=data, _external=True))
            # redirect(url_for('send_welcome_message', email=data, _external=True))
            # redirect(url_for('send_confirmation_link', phone=data, _external=True))
            return jsonify({'status': 'done', 'result': str(new_user.toDict()).replace("'", '"')})


class ActivityStories(Resource):

    @jwt_required()
    def get(self, start, category=None):
        stories = get_stories(current_identity, start, category)
        if stories != 'failed':
            return jsonify(buildJson("Story", stories))
        return jsonify({'status': 'failed', 'result': 'no stories found'})

    @jwt_required()
    def post(self):
        files = request.files
        story = request.json
        status = post(current_identity, story, files)
        if status == 'done':
            return jsonify({'status': 'done', 'result': 'post successful'})
        return jsonify({'status': 'failed'})

    @jwt_required()
    def put(self):
        story = request.json
        files = request.files
        status = edit_post(current_identity, story, files)
        if status == 'done':
            return jsonify({'status': 'done', 'result': 'post update successful'})
        return jsonify({'status': 'failed'})

    @jwt_required()
    def delete(self, storyid):
        status = deleteIt(current_identity, storyid=storyid)
        if status == 'done':
            return jsonify({'status': 'done', 'result': 'post delete successful'})
        return jsonify({'status': 'failed'})


class ActivityStoryItem(Resource):

    @jwt_required()
    def get(self, storyid):
        pass

    def delete(self, storyid):
        pass


class ActivityComments(Resource):

    @jwt_required()
    def get(self, method, limit):
        pass

    def post(self, story):
        pass

    def put(self, story):
        pass

    def delete(self, storyid):
        pass


class ActivityFriends(Resource):

    @jwt_required()
    def get(self):
        user = current_identity
        added_friends = Friends.query.filter(Friends.user_id == user.id, Friends.pending == 'done').all()
        other_friends = Friends.query.filter(Friends.friend_id == user.id, Friends.pending == 'done').all()
        friends = added_friends + other_friends
        return jsonify(buildJson('friend', friends))

    def post(self, friend):
        pass

    def put(self, friend):
        pass

    def delete(self, friend_id):
        pass


class ActivityFollowers(Resource):

    @jwt_required()
    def get(self, friend_id):
        user = current_identity
        ufriends = Friends.query.filter(Friends.user_id == user.id, Friends.pending == 'done').all()
        ofriends = Friends.query.filter(Friends.friend_id == user.id, Friends.pending == 'done').all()
        friends = ufriends + ofriends
        return jsonify(dict(friends))

    def post(self, friend):
        pass

    def put(self, friend):
        pass

    def delete(self, friend_id):
        pass


class ActivityFriendFinder(Resource):

    @jwt_required()
    def get(self, friend_id):
        pass

    def post(self, friend):
        pass

    def put(self, friend):
        pass

    def delete(self, friend_id):
        pass


class ActivityFriendRequest(Resource):

    @jwt_required()
    def get(self, friend_id):
        pass

    def post(self, friend):
        pass

    def put(self, friend):
        pass

    def delete(self, friend_id):
        pass


class ActivityChats(Resource):

    @jwt_required()
    def get(self, chat_id):
        return Messages.query.all()

    def post(self, chat):
        pass

    def put(self, chat):
        pass

    def delete(self, chat_id):
        pass


class ActivityMessages(Resource):

    @jwt_required()
    def get(self, chat_id):
        return Messages.query.all()

    def post(self, chat):
        pass

    def put(self, chat):
        pass

    def delete(self, chat_id):
        pass


class ActivityNotifications(Resource):

    @jwt_required()
    def get(self):
        user = current_identity
        notifications = Notifications.query.filter_by(note_receiver=user.id).all()
        return jsonify({'status': 'done', 'result': str(buildJson('notification', notifications)).replace("'", '"')})

    @jwt_required()
    def post(self, notification):
        notifications = Notifications.query.filter_by(note_id=notification).all()
        return jsonify({'status': 'done', 'result': str(buildJson('notification', notifications)).replace("'", '"')})


class ActivityGallery(Resource):

    @jwt_required()
    def get(self, gallery_id):
        user = current_identity
        gallery_items = get_gallery(user, get='all')
        return jsonify({'status': 'done', 'result': gallery_items})

    def post(self, gallery):
        pass

    def put(self, gallery):
        pass

    def delete(self, gallery_id):
        pass


class ActivityExplore(Resource):

    @jwt_required()
    def get(self, search):
        user = current_identity
        explore_seen[user.id] = []
        if not search == '' or search is not None:
            search_discover = Storys.query.filter((and_(Storys.privacy == 'public')), Storys.story_content
                                                  .like("%{}%".format(search))) \
                .order_by(desc('timestamp')).limit(50).all()
            return jsonify({'status': 'done'})
        discover = get_stories(user, start=0, explore=True)
        return jsonify({'status': 'done', 'data': discover})


class ActivitySearch(Resource):

    @jwt_required()
    def get(self, data):
        if data == '' or data == ' ' or data is None:
            return jsonify({'status': 'failed'})
        user_results = Users.query.filter(or_(Users.firstname.like("%{}%".format(data)),
                                              Users.lastname.like("%{}%".format(data)),
                                              Users.username.like("%{}%".format(data)),
                                              Users.email.like("%{}%".format(data)))).all()
        return jsonify({'status': 'done', 'result': str(jsonify(dict(user_results)))})


class RequestProcessor(Resource):

    @jwt_required()
    def post(self):
        process = processor(current_identity, request.json)
        return process


########################################################################
########################################################################
# ROUTES DECLARATION
########################################################################


api.add_resource(Authenticate, '/login')
api.add_resource(ActivitySignup, '/signup/<firstname>/<lastname>/<email>/<username>/<password>')
api.add_resource(UserManager, '/manage/get_user/<username>')
api.add_resource(ActivityStories,
                 '/get_stories/<start>/<category>', '/post_story',
                 '/update_story', '/delete_story/<storyid>'
                 )
api.add_resource(ActivityFriends, '/friends')
api.add_resource(ActivityNotifications, '/notifications/<method>/<limit>')
api.add_resource(RequestProcessor, '/process')

api.add_resource(Test, '/test')

# @app.route('/view_post/<postid>', methods=['POST', 'GET'])
# @app.route('/view_mutual_friends/<friendid>', methods=['POST', 'GET'])
# @app.route('/view_profile/<username>', methods=['POST', 'GET'])
# @app.route('/change_password/<old_password>/<new_password>', methods=['POST', 'GET'])
# @app.route('/forgot/email/<user_email>', methods=['POST', 'GET'])
# @app.route('/forgot/phone/<user_phone>', methods=['POST', 'GET'])
# @app.route('/reset_password/<token>/<new_password>', methods=['POST', 'GET'])
# @app.route('/help/<help_search>', methods=['POST', 'GET'])
# @app.route('/add_help/<helptopic>/<helpcontent>', methods=['POST'])
# @app.route('/verify/<data>', methods=['POST', 'GET'])
# @app.route('/send_welcome')
# @app.route('/send_link_email/<email>')
# @app.route('/send_link_phone/<phone>')
# @app.route('/confirm_email/<token>')
# @app.route('/confirm_phone/<token>', methods=['POST'])


if __name__ == "__main__":
    connect_to_db(app)
    # socketio.run(app, debug=True)
    socketio.run(app, host="192.168.137.1", port=80, debug=True)
