import os
import datetime
from operator import attrgetter
import flask_admin as admins
from sqlalchemy.dialects.postgresql import JSONB
from database import Messages, Comments, Likes, Comment_likes, Unread_Messages as UM, Slidestore
from database import Users, Friends, Follows, Posts, Notifications, Gallery, Help
from database import db, connect_to_db
from flask import Flask, redirect, render_template, url_for, flash, g, jsonify, request, abort
from flask_admin import Admin, helpers
from flask_admin.base import expose
from flask_admin.contrib import sqla
from flask_admin.contrib.sqla.view import ModelView
from flask_bootstrap import Bootstrap
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_mail import Mail, Message
from flask_socketio import SocketIO, send, emit, join_room, leave_room, disconnect
from flask_uploads import UploadSet, configure_uploads, extension, patch_request_class, IMAGES, AUDIO, DOCUMENTS
from flask_wtf import FlaskForm
from itsdangerous import URLSafeTimedSerializer, URLSafeSerializer, SignatureExpired, BadSignature
from sqlalchemy.sql.expression import desc, and_, or_, func, cast
from twilio_app import twilio_send
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms import StringField, PasswordField, BooleanField, widgets, MultipleFileField, form, fields, validators
from wtforms.fields.html5 import DateField
from wtforms.validators import InputRequired, Length, Email, ValidationError, EqualTo




app = Flask(__name__)
app.config['SECRET_KEY'] = "iamotc&ifuckingrule@#techup#"
# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://jfvhvyrisvbkzk:8134222a346acf6484020a4c07a805b0fa6e4f6ca97b3f51105a745b601f8027@ec2-107-21-98-165.compute-1.amazonaws.com:5432/d4s49sa8pb9hb'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:Asdwe111@localhost:5432/chatapp'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config.from_pyfile('config.cfg')
Bootstrap(app)
socketio = SocketIO(app)
mail = Mail(app)
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
online_users = {}
hang_users = {}
chat_buddy = {}
explore_seen = {}
ago_list = {}

# ********VALIDILITY FUNCTIONS**********#

def user_exists(form, field):
    user = get_user(username=form.username.data)
    if user:
        raise ValidationError('User with this name already exists.')


def email_exists(form, field):
    email = get_user(email=form.email.data)
    if email:
        raise ValidationError('User with this email already exists.')


def tel_exists(form, field):
    tel = Users.query.filter_by(phone=form.phone.data).first()
    if tel:
        raise ValidationError('Number already used.')


def input_not_exist(form, field):
    email = get_user(email=form.input.data)
    phone = get_user(phone=form.input.data)
    try:
        if not email:
            if not phone:
                raise ValidationError('User does not exists.')
    except Exception:
        raise ValidationError('User does not exists, please register')


def invalid(form, field):
    user = get_user(username=form.username.data)
    e_user = get_user(email=form.username.data)
    p_user = get_user(phone=form.username.data)
    try:
        if not user or not check_password_hash(user.password, form.password.data):
            if not e_user or not check_password_hash(e_user.password, form.password.data):
                if not p_user or not check_password_hash(p_user.password, form.password.data):
                    raise ValidationError('Invalid username or password!')
    except Exception:
        raise ValidationError('Invalid username or password')


# *******APP FUNCTIONS******#

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
        post = Posts.query.filter_by(post_id=sectionid).first()
        if post:
            check = check_if_liked(user, sectionid)
            if check == False:
                new_like = Likes(post_id=sectionid, liker=user.id, timestamp=datetime.datetime.now())
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
                like = Comment_likes.query.filter(Comment_likes.comment_id == sectionid, Comment_likes.liker == user.id).first()
                if like:
                    db.session.delete(like)
                    db.session.commit()
                    return 'done'
                return 'failed'
            return 'failed'
        return 'failed'
    else:
        post = Posts.query.filter_by(post_id=sectionid).first()
        if post:
            check = check_if_liked(user, sectionid)
            if check == True:
                like = Likes.query.filter(Likes.post_id == sectionid, Likes.liker == user.id).first()
                if like:
                    db.session.delete(like)
                    db.session.commit()
                    return 'done'
                return 'failed'
            return 'failed'
        return 'failed'


def comment(user, postid, content):
    post = Posts.query.filter_by(post_id=postid).first()
    if post:
        if  content.isspace() == False and content != '' :
            comment = Comments(user_id=user.id, post_id=postid, comment_content=content, timestamp=datetime.datetime.now())
            db.session.add(comment)
            db.session.commit()
            return 'done'
        return 'failed'
    return 'failed'

def check_if_liked(user, sectionid, comment=None):
    if comment:
        check = Comment_likes.query.filter(Comment_likes.liker == user.id, Comment_likes.comment_id == sectionid).first()
        if check:
            return True
        else:
            return False
    else:
        check = Likes.query.filter(Likes.liker == user.id, Likes.post_id == sectionid).first()
        if check:
            return True
        else:
            return False


def get_user(userid=None, username=None, email=None, phone=None, noteid=None, postid=None, messageid=None, commentid=None):
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
    elif postid:
        if type(postid) == int:
            try:
                check = Posts.query.filter_by(post_id=postid).first()
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
        likers = Likes.query.filter(Likes.post_id == sectionid).all()
    if count:
        count_likes = len(likers)
        return count_likes
    else:
        return likers


def get_comments(postid, count=None):
    commenters = Comments.query.filter(Comments.post_id == postid).all()
    if count:
        count_comments = Comments.query.filter(Comments.post_id == postid).count()
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


def get_news_feed(user, start, only=None, explore=None):
    x = 0
    index = start
    stream = []
    streams = []
    ago = []
    lists = friends_id_list(user)
    if only:
        limit = 3
        streamz = Posts.query.filter(Posts.user_id == user.id, Posts.privacy == 'public').order_by(desc('timestamp')).all()
    elif explore:
        lists.append(user.id)
        seen = explore_seen[user.id]
        streams = Posts.query.filter(Posts.user_id.notin_(lists), Posts.post_id.notin_(seen)).order_by(func.random()).limit(3).all()
        if streams != []:
            for stream in streams:
                seen.append(stream.post_id)
            return streams
        return 'failed'
    else:
        stream += Posts.query.filter_by(user_id=user.id).all()
        for ids in lists:
            get_post = Posts.query.filter_by(user_id=ids).order_by(desc('timestamp')).limit(10).all()
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
                    for  data in streams:
                        ago.append(data.post_id)
                    ago_list[user.id] = ago
                    streams.append('reachedMax')
                    return streams
                    break
                else:
                    x += 1
            except Exception:
                return 'failed'
        for  data in streams:
            ago.append(data.post_id)
        ago_list[user.id] = ago
        return streams


def get_messages(user, friend, start):
    messages = Messages.query.filter(or_((and_(Messages.sender_id==user.id, Messages.receiver_id==friend)),(and_(Messages.sender_id==friend, Messages.receiver_id==user.id)))).order_by(desc('timestamp')).all()
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
        document = tuple('pdf txt ppt pptx xlsx zip htm html tar rar gz py pyd js exe cpp c'.split())
        print(media)
        for file in media:
            print(file)
            print(file.mimetype)
            name = file.filename
            ext = extension(name)
            postname = name[:-(len(ext)+1)]
            
            if used_as == 'slide':
                filetype = ext
                filename = slide.save(file, name='Slide.')
                path = "/static/uploads/slides/{}".format(filename)
                return {'status': 'done', 'ext': ext, 'filename': filename, 'path': path}
            elif ext.lower() in IMAGES:
                filetype = 'photo'
                filename = photos.save(file, name='Photo.')
                path = "/static/uploads/photos/{}".format(filename)
                paths.append(path)
            elif ext.lower() in AUDIO or ext.lower() in audio :
                filetype = 'audio'
                filename = audios.save(file, name='Audio.')
                path = "/static/uploads/audios/{}".format(filename)
                paths.append(path)
            elif ext.lower() in VIDEO:
                filetype = 'video'
                filename = videos.save(file, name='Video.')
                path = "/static/uploads/videos/{}".format(filename)
                paths.append(path)
            elif ext.lower() in DOCUMENTS or ext.lower() in document:
                filetype = 'document'
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
        new_upload = Gallery(user_id=user.id, upload_type=filetype, upload_used_as=used_as, upload_path=paths, privacy=privacy, timestamp=datetime.datetime.now())
        db.session.add(new_upload)
        db.session.commit()
        if used_as == 'profile_pic':
            user.profile_pic = path
            db.session.add(user)
            db.session.commit()
            return {'result': 'done', 'path': paths, 'filetype': filetype, 'postname': postname}
        return {'result': 'done', 'path': paths, 'filetype': filetype, 'postname': postname}
    except Exception as e:
        print('error :'+str(e))
        return {'result': 'failed'}


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
        notes1 = Notifications.query.filter(Notifications.user_id == friend, Notifications.note_receiver == user.id, (or_(Notifications.note_header == 'FRQ', Notifications.note_header == 'AFR'))).all() 
        notes2 = Notifications.query.filter(Notifications.user_id == user.id, Notifications.note_receiver == friend, (or_(Notifications.note_header == 'FRQ', Notifications.note_header == 'AFR'))).all()
        if notes1 or notes2:
            for note in (notes1 + notes2):
                db.session.delete(note)
            db.session.commit()
            return 'done'
        return 'ok'
    elif action == 'follow' or action == 'unfollow':
        notes = Notifications.query.filter(Notifications.user_id == user.id, Notifications.note_receiver == friend, Notifications.note_header == 'FLW').all()
        if notes:
            for note in notes:
                db.session.delete(note)
            db.session.commit()
            return 'done'
        return 'done'
    elif action == 'accept' or action == 'decline':
        notes = Notifications.query.filter(Notifications.user_id == user.id, Notifications.note_receiver == friend, Notifications.note_header == 'AFR').all()
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
            notes1 = Notifications.query.filter(Notifications.user_id == note.note_receiver, Notifications.note_receiver == note.note_id, Notifications.note_header == 'AFR').all() 
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
        notes = Notifications.query.filter(Notifications.user_id == friend, Notifications.note_receiver == user.id, Notifications.note_header == 'FRQ').all() 
        if notes:
            for note in notes:
                db.session.delete(note)
            db.session.commit()
            return 'done'
        return 'done'
    elif action == 'get_messages':
        messages = Messages.query.filter(Messages.sender_id == friend, Messages.receiver_id == user.id, Messages.seen == 0).all() 
        if messages:
            for message in messages:
                message.seen = 1
                db.session.add(message)
            db.session.commit()
            return 'done'
        return 'failed'
    else:
        return 'failed'


def deleteIt(user, postid=None, noteid=None, commentid=None, messageid=None, galleryid=None, path=None):
    if postid:
        post = Posts.query.filter_by(post_id=postid).first()
        likes = Likes.query.filter_by(post_id=postid).all()
        comments = Comments.query.filter_by(post_id=postid).all()
        if post:
            if post.user_id == user.id:
                if likes:
                    for result in likes:
                        db.session.delete(result)
                if comments:
                    for result in comments:
                        deleteIt(user, commentid=result.comment_id)
                if (post.post_content['media'][0])['filetype'] != 'None': 
                    for media in post.post_content['media']:
                        file = Gallery.query.filter(Gallery.user_id==user.id, Gallery.upload_used_as=='post', Gallery.upload_path == cast((media['path']), JSONB)).first()
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
        person = get_user(postid=comment.post_id)
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
                print("deleting file at"+file)
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
    day= int(d)
    h = dt[11:13]
    hour = int(h)
    mn = dt[14:16]
    minute = int(mn)
    s = dt[17:19]
    second = int(s)
    ms = dt[20:26]
    microsecond = int(ms)
    period = datetime.datetime.now()-datetime.datetime(year, month, day, hour, minute, second, microsecond)
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



def get_pages(user, get=None):
    pass


def get_clubs(user, get=None):
    pass


def get_games(user, get=None):
    pass


def apps_func(app, action=None, this=None, update=None, value=None, user=None):
    if app == 'slidestore':
        if action == 'search':
            process = Slidestore.query.filter(or_(Slidestore.slide_name.like("%{}%".format(this)), Slidestore.slide_type.like("%{}%".format(this)),  Slidestore.level.like("%{}%".format(this)),  Slidestore.slide_type.like("%{}%".format(this)), Slidestore.course.like("%{}%".format(this)))).all()
            if process:
                return process
            return 'failed'
        elif action == 'delete':
            slide = Slidestore.query.filter(Slidestore.slide_name == this, Slidestore.publisher == user.id).first() 
            if slide:
                file_path = os.getcwd() + slide.slide_path
                os.remove(file_path)
                db.session.delete(slide)
                db.session.commit()
                return 'done'
            return 'failed'
        elif action == 'update':
            slide = Slidestore.query.filter(Slidestore.slide_name == this, Slidestore.publisher == user.id).first() 
            if slide:
                if update == 'name':
                    slide.slide_name == value
                elif update == 'type':
                    slide.slide_type == value 
                elif update == 'file':
                    file_path = os.getcwd() + slide.slide_path
                    os.remove(file_path)
                    slide.slide_path = value
                else:
                    pass
                db.session.add(slide)
                db.session.commit()
                return 'done'
            return 'failed'
        else:
            pass

            

def get_gallery(user, get='all'):
    if get == 'all':
        all_gallery = Gallery.query.filter(Gallery.user_id == user.id).order_by(desc(Gallery.timestamp)).all()
        return all_gallery
    elif get == 'pics':
        pics_gallery = Gallery.query.filter(Gallery.user_id == user.id, (or_(Gallery.upload_type == 'photo', Gallery.upload_type == 'photo'))).order_by(desc(Gallery.timestamp)).all()
        return pics_gallery
    elif get == 'auds':
        pics_gallery = Gallery.query.filter(Gallery.user_id == user.id, Gallery.upload_type == 'audio').order_by(desc(Gallery.timestamp)).all()
        return pics_gallery
    elif get == 'vids':
        vids_gallery = Gallery.query.filter(Gallery.user_id == user.id, Gallery.upload_type == 'video').order_by(desc(Gallery.timestamp)).all()
        return vids_gallery
    elif get == 'docs':
        vids_gallery = Gallery.query.filter(Gallery.user_id == user.id, Gallery.upload_type == 'document').order_by(desc(Gallery.timestamp)).all()
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
    user = current_user
    if nc:
        notices = Notifications.query.filter(Notifications.note_receiver == user.id, Notifications.seen == None).count()
        return notices
    elif pc:
        # new_post = Posts.query.filter(user_id=user.id).order_by(desc(Posts.timestamp)).count()
        pass
    elif mc:
        count = 0
        messages = UM.query.filter_by(receiver_id=user.id).all()
        for message in messages:
            count += message.count
        return count
    else:
        return 'failed'


def unread_messages(sender, friend, action=None):
    user = sender
    if action == 'add':
        if friends_checker(user, friend) == True:
            check = UM.query.filter(UM.sender_id==user.id, UM.receiver_id==friend).first()
            if check:
                check.count = check.count + 1
                db.session.add(check)
                db.session.commit()
                return 'done'
            else:
                new_um = UM(sender_id=user.id, receiver_id=friend, count=1)
                db.session.add(new_um)
                db.session.commit()
                return 'done'
        else:
            return 'failed'
    elif action == 'get':
        check = UM.query.filter(UM.sender_id==friend, UM.receiver_id==user.id).first()
        try:
            if check != None:
                if check.count > 0:
                    return check.count
        except Exception:
            pass
    elif action == 'reset':
        reset = UM.query.filter(UM.sender_id==user.id, UM.receiver_id==friend).first()
        if reset:
            reset.count = 0
            db.session.add(reset)
            db.session.commit()
            return 'done'
    else:
        return 'error'

            



# ******END OF FUNCTIONS*****##
# ******Sending modules in jinjA*****#

app.jinja_env.globals.update(len=len)
app.jinja_env.globals.update(countit=countit)
app.jinja_env.globals.update(time_ago=time_ago)
app.jinja_env.globals.update(unread_messages=unread_messages)
app.jinja_env.globals.update(friends_checker=friends_checker)
app.jinja_env.globals.update(friends_id_list=friends_id_list)
app.jinja_env.globals.update(check_if_liked=check_if_liked)
app.jinja_env.globals.update(check_if_following=check_if_following)
app.jinja_env.globals.update(get_followers=get_followers)
app.jinja_env.globals.update(get_pages=get_pages)
app.jinja_env.globals.update(get_likes=get_likes)
app.jinja_env.globals.update(get_comments=get_comments)
app.jinja_env.globals.update(get_user=get_user)
app.jinja_env.globals.update(get_online_friends=get_online_friends)
app.jinja_env.globals.update(get_news_feed=get_news_feed)
app.jinja_env.globals.update(get_suggestions=get_suggestions)
app.jinja_env.globals.update(get_mutual_friends=get_mutual_friends)
app.jinja_env.globals.update(get_friend_requests_from_user=get_friend_requests_from_user)
app.jinja_env.globals.update(get_friend_requests_to_user=get_friend_requests_to_user)


# ********FORMS************#

class FResetForm(FlaskForm):
    new_password = PasswordField('New password', validators=[InputRequired(), Length(min=7, max=80)])
    confirm_password = PasswordField('Confirm password', validators=[InputRequired(), Length(min=7, max=80), EqualTo('new_password', message="Password's don't match")])


class CResetForm(FlaskForm):
    old_password = PasswordField('Current password', validators=[InputRequired(), Length(max=80)])
    new_password = PasswordField('New password', validators=[InputRequired(), Length(min=7, max=80)])
    confirm_password = PasswordField('Confirm password', validators=[InputRequired(), Length(min=7, max=80), EqualTo('new_password', message="Password's don't match")])


class PResetForm(FlaskForm):
    user_phone = StringField('Enter your phone number', widget=widgets.Input(input_type="tel"), validators=[InputRequired(), Length(max=13)])


class EResetForm(FlaskForm):
    user_email = StringField('Enter your registered email', validators=[InputRequired(), Email(message="Invalid Email"), Length(max=40)])


class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=5, max=32)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=7, max=80), invalid])
    remember = BooleanField('remember me')


class SignupForm(FlaskForm):
    firstname = StringField('firstname', validators=[InputRequired(), Length(max=32)])
    lastname = StringField('lastname', validators=[InputRequired(), Length(max=32)])
    dateofbirth = DateField('date of birth', format="%Y-%m-%d")
    email = StringField('email', validators=[InputRequired(), Email(message="Invalid Email"), Length(max=40), email_exists])
    # country_code = StringField('country', validators=[InputRequired(), Length(max=4)])
    phone = StringField('phone', widget=widgets.Input(input_type="tel"), validators=[tel_exists])
    username = StringField('username', validators=[InputRequired(), Length(min=5, max=32), user_exists])
    password = PasswordField('password', validators=[InputRequired(), Length(min=7, max=80)])
    passwordrepeat = PasswordField('confirm password', validators=[InputRequired(), Length(min=7, max=80), EqualTo('password', message="password's don't match")])


class SearchForm(FlaskForm):
    search = StringField('', validators=[InputRequired(), Length(min=3, max=32)])


class PostForm(FlaskForm):
    postbox = StringField('', validators=[InputRequired(), Length(max=3000)])


class UploadForm(FlaskForm):
    media = MultipleFileField('', validators=[InputRequired()])


class ConfirmForm(FlaskForm):
    input = StringField('Enter email or phone number', validators=[InputRequired(), Length(max=40), input_not_exist])


class HelpForm(FlaskForm):
    help_search = StringField('', validators=[InputRequired(), Length(max=200)])


class AddHelpForm(FlaskForm):
    helptopic = StringField('New Help Topic', validators=[Length(max=90)])
    helpcontent = StringField('Help Content', validators=[Length(max=10000)])


class SettingsForm(FlaskForm):
    settings = StringField('', validators=[InputRequired(), Length(max=20)])


# ********MAIN ROUTES***********


@app.before_request
def before_request():
    g.user = current_user


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


# *******ADMIN ROUTE***********#

# Define login and registration forms (for flask-login)
class AdminLoginForm(form.Form):
    admin_name = fields.StringField(validators=[validators.required()])
    password = fields.PasswordField(validators=[validators.required()])

    def validate_login(self, field):
        user = self.get_user()
        if user:
            if not check_password_hash(user.password, self.password.data):
                raise validators.ValidationError('Invalid password')
        raise validators.ValidationError('Invalid user')

    def get_user(self):
        return db.session.query(Users).filter_by(username=self.admin_name.data).first_or_404()


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

    @expose('/login/', methods=('GET', 'POST'))
    def login_view(self):
        form = AdminLoginForm(request.form)
        if helpers.validate_form_on_submit(form):
            user = form.get_user()
            if user.user_status == 'goduser':
                login_user(user)
            return redirect(url_for('.login_view'))

        if current_user.is_authenticated:
            return redirect(url_for('.index'))
        self._template_args['form'] = form
        return super(MyAdminIndexView, self).index()

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
admin.add_view(MyModelView(Posts, db.session))
admin.add_view(MyModelView(Notifications, db.session))
admin.add_view(HelpAdmin(Help, db.session))
admin.add_view(MyModelView(Gallery, db.session))
admin.add_view(MyModelView(Likes, db.session))
admin.add_view(MyModelView(Messages, db.session))
admin.add_view(MyModelView(Comments, db.session))
admin.add_view(MyModelView(Comment_likes , db.session))


# ****END OF ADMIN ROUTES*******#

@app.route('/')
def home():
    return render_template("home.html")


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if request.method == "POST":
        if form.validate_on_submit():
            hashpass = generate_password_hash(form.password.data, method='sha256')
            intro_about = 'My name is ' + form.firstname.data + ' ' + form.lastname.data + '. but you can call me ' + form.username.data + '.'
            new_user = Users(username=form.username.data, password=hashpass, firstname=form.firstname.data,
                             lastname=form.lastname.data, dateofbirth=form.dateofbirth.data, email=form.email.data,
                             phone=form.phone.data, about=intro_about, user_status='normal')
            db.session.add(new_user)
            db.session.commit()
            # email = form.email.data
            # phone = form.phone.data
            # redirect(url_for('send_confirmation_email', email=data, _external=True))
            # redirect(url_for('send_welcome_message', email=data, _external=True))
            # redirect(url_for('send_confirmation_link', phone=data, _external=True))
            flash("Your Account Has Been Created", "success")
            return redirect(url_for('login'))
        return render_template("signup.html", form=form)
    return render_template("signup.html", form=form)


@app.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    user = get_user(username=form.username.data)
    e_user = get_user(email=form.username.data)
    p_user = get_user(phone=form.username.data)
    if form.validate_on_submit():
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                return redirect(url_for('timeline'))
        elif e_user:
            if check_password_hash(e_user.password, form.password.data):
                login_user(e_user, remember=form.remember.data)
                return redirect(url_for('timeline'))
        elif p_user:
            if check_password_hash(p_user.password, form.password.data):
                login_user(p_user, remember=form.remember.data)
                return redirect(url_for('timeline'))
        else:
            flash('Cant find user!, details might be wrong', 'error')
            return render_template("login.html", form=form)
    return render_template("login.html", form=form)


@app.route('/timeline', methods=['POST', 'GET'])
@login_required
def timeline():
    user = current_user
    form = PostForm()
    return render_template("timeline.html", form=form, user=user)


@app.route('/messages', methods=['POST', 'GET'])
@login_required
def messages():
    user = current_user
    return render_template('messages.html', user=user)


@socketio.on('connected')
@login_required
def user_connected():
    user = current_user
    online_users[user.id] = request.sid
    response = {'username': user.username, 'userid': user.id}
    friends = get_online_friends(user)
    if friends != []:
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
    online_users[user.id]=sid
    room = 'allusersgroupmessage'
    if msg.lower() == '@commands':
        response = {'username': 'Commands', 'message': '@clear -- clear screen <br/> @users -- count online hangers <br/> @leave -- leave group  <br/> @friends -- show friends in group <br/> @bot -- automate features [log old messages for you etc]'}
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
    online_users[user.id]=sid
    chat_buddy[user.id] = 0
    join_room(room, sid=sid)
    response = {'username': user.username, 'message': "What's Hanging?"}
    emit('newaugMessage', response, room=room, include_self=False)


@socketio.on('private_message', namespace='/private')
@login_required
def handle_private_message(data):
    user = current_user
    online_users[user.id]=request.sid
    recipient_id = int(data['userid'])
    buddy = get_user(userid=recipient_id)
    message = data['message']
    print(message)
    try:
        recipient_sid = online_users[recipient_id]   
    except Exception:
        pass
    if message != '' and message.isspace() != True :
        new_message = Messages(sender_id=user.id, receiver_id=recipient_id, message_content=message, timestamp=datetime.datetime.now())
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
    user = current_user
    if is_banned(user.id):
        disconnect()
    else:
        #send(msg, room=room)
        pass


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
                post = Posts.query.filter_by(post_id=id_).first()
                if post:
                    time_used = time_ago(post.timestamp)
                    response.append({'section': 'ago{}'.format(id_), 'time': time_used})
            emit('time_spent', response)
    except Exception:
        pass
    


@socketio.on_error_default
def default_error_handler(e):
    print(request.event["message"]) # "my error event"
    print(request.event["args"]) # (data)
    print(e)


@app.route('/post', methods=['POST', 'GET'])
@login_required
def post():
    user = current_user
    form = PostForm()
    src = [{'filetype': 'None', 'path': 'None'}]
    privacy = request.form['privacy']
    if 'media' in request.files:
        media = request.files.getlist('media')
        process = upload(user, media, privacy=privacy, used_as='post')
        if process['result'] == 'done':
            path = process['path']
            type_ =  process['filetype']
            postname = process['postname']
            src = [{'path':path, 'filetype':type_, 'filename': postname}]
        pass
    if form.validate_on_submit():
        new_post = Posts(user_id=user.id, post_content={'post': form.postbox.data, 'media': src}, privacy=privacy, timestamp=datetime.datetime.now())
        db.session.add(new_post)
        db.session.commit()
        flash("Post successfull!", "success")
        return redirect(url_for('timeline'))
    return redirect(url_for("timeline"))


@app.route('/_post', methods=['POST'])
@login_required
def post_from_profile():
    user = current_user
    form = PostForm()
    src = [{'filetype': 'None', 'path': 'None'}]
    privacy = request.form['privacy']
    print('at route /p_post')
    if request.method == 'POST':
        print('working')
        if 'media' in request.files:
            media = request.files.getlist('media')
            process = upload(user, media, privacy=privacy, used_as='post')
            if process['result'] == 'done':
                path = process['path']
                type_ =  process['filetype']
                postname = process['postname']
                src = [{'path':path, 'filetype':type_, 'filename': postname}]
            pass
        if form.validate_on_submit():
            new_post = Posts(user_id=user.id, post_content={'post': form.postbox.data, 'media': src}, privacy=privacy, timestamp=datetime.datetime.now())
            db.session.add(new_post)
            db.session.commit()
            flash("Post successfull!", "success")
            return redirect(url_for('profile', username=user.username))
        return redirect(url_for("profile", username=user.username))


    
@app.route('/edit/<postid>', methods=['POST', 'GET'])
@login_required
def edit_post(postid):
    form = PostForm()
    user = current_user
    old_post = Posts.query.filter_by(post_id=postid).first()
    if user.id == old_post.user_id:
        if form.validate_on_submit():
            edit = old_post
            if edit:
                post_media = (edit.post_content)['media'] #check if new media then change details for media else pass
                privacy = request.form['privacy']
                if 'media' in request.files:
                    media = request.files.getlist('media')
                    old_media = Gallery.query.filter(Gallery.user_id==user.id, Gallery.upload_used_as=='post', Gallery.upload_path == cast(((((edit.post_content)['media'])[0])['path']), JSONB)).first() 
                    deleteIt(user, galleryid=old_media.gallery_id)
                    process = upload(user, media, privacy=privacy, used_as='post')
                    if process['result'] == 'done':
                        path = process['path']
                        type_ =  process['filetype']
                        postname = process['postname']
                        post_media = [{'path':path, 'filetype':type_, 'filename': postname}]
                    pass
                edited_pc = {'post': form.postbox.data, 'media': post_media}
                edit.post_content = edited_pc
                edit.privacy = privacy
                edit.timestamp = datetime.datetime.now()
                edit.edited = 'true'
                db.session.add(edit)
                db.session.commit()
            flash("The post has been succesfully updated", 'success')
            return redirect(url_for('timeline'))
        return render_template('edit-post.html', form=form, old_post=old_post)
    flash("you don't have permission to edit this!!!", 'error')
    return redirect(url_for('timeline'))


@app.route('/view_post/<postid>', methods=['POST', 'GET'])
@login_required
def view_post(postid):
    user = current_user
    return render_template("view-posts.html", user=user, postid=postid)


@app.route('/view_mutual_friends/<friendid>', methods=['POST', 'GET'])
@login_required
def view_mutual_friends(friendid):
    user = current_user
    friend = get_user(userid=friendid)
    if friend:
        mutual_friends = get_mutual_friends(user, friend)
        return render_template("view-mutuals.html", user=user, mutual_friends=mutual_friends)
    return redirect(url_for('friends'))


@app.route('/profile/<username>', methods=['POST', 'GET'])
@login_required
def profile(username):
    form = PostForm()
    user = current_user
    # add tagged posts with user
    return render_template("profile.html", form=form, user=user)


@app.route('/view_profile/<userid>/<username>', methods=['POST', 'GET'])
@login_required
def view_profile(userid, username):
    visitor = current_user
    user = get_user(userid=int(userid))
    if user:
        if user.id != visitor.id:
            posted = Posts.query.filter(Posts.user_id == user.id, Posts.privacy == 'public').limit(3).all()
            return render_template("view-profile.html", user=visitor, friends_posts=posted, friend=user)
        return redirect(url_for('profile', username=visitor.username))
    return redirect(url_for('friends'))


@app.route('/friends', methods=['POST', 'GET'])
@login_required
def friends():
    user = current_user
    ufriends = Friends.query.filter(Friends.user_id == user.id, Friends.pending == 'done').all()
    ofriends = Friends.query.filter(Friends.friend_id == user.id, Friends.pending == 'done').all()
    return render_template('friends.html', user=user, ufriends=ufriends, ofriends=ofriends)


@app.route('/notifications', methods=['POST', 'GET'])
@login_required
def notification():
    user = current_user
    notices = Notifications.query.filter_by(note_receiver=user.id).all()
    return render_template('notification.html', user=user, notices=notices)


@app.route('/gallery', methods=['POST', 'GET'])
@login_required
def gallery():
    user = current_user
    gallery_items = get_gallery(user, get='all')
    return render_template("gallery.html", user=user, gallery_items=gallery_items)


@app.route('/apps', methods=['POST', 'GET'])
@login_required
def apps():
    user = current_user
    return render_template("apps.html", user=user)


@app.route('/apps/gpa-calc', methods=['POST', 'GET'])
@login_required
def gpa_calculator():
    user = current_user
    return render_template("gpa-calc.html", user=user)


@app.route('/apps/timetable-guru', methods=['POST', 'GET'])
@login_required
def timetable_guru():
    user = current_user
    return render_template("tt-guru.html", user=user)


@app.route('/apps/slidestore', methods=['POST', 'GET'])
@login_required
def slidestore():
    user = current_user
    return render_template("slidestore.html")


@app.route('/apps/slidestore/add_slide', methods=['POST'])
@login_required
def add_slide():
    user = current_user
    form = AddSlideForm()
    if form.validate_on_submit():
        if user.user_status == 'helper' or user.user_status == 'god_user':
            if 'slide' in request.files:
                media = request.files.getlist('slide')
                process = upload(user, media, used_as='slide')
                if process['status'] == 'done':
                    ext = process['ext']
                    path = process['path']
                    filename = process['filename']
                    new_slide = Slidestore(level=form.level.data, course=form.course.data, slide_type=ext, slide_path=path, slide_name=filename, publisher=user.id)
                    db.session.add(new_slide)
                    db.session.commit()
                    return redirect(url_for('slidestore'))


@app.route('/games', methods=['POST', 'GET'])
@login_required
def games():
    user = current_user
    return render_template("games.html", user=user)


@app.route('/clubs', methods=['POST', 'GET'])
@login_required
def clubs():
    user = current_user
    return render_template("clubs.html", user=user)


@app.route('/pages', methods=['POST', 'GET'])
@login_required
def pages():
    user = current_user
    return render_template("pages.html", user=user)


@app.route('/pending', methods=['POST', 'GET'])
@login_required
def pending():
    user = current_user
    return render_template("pending.html", user=user)


@app.route('/explore', methods=['POST', 'GET'])
@login_required
def explore():
    user = current_user
    form = SearchForm()
    explore_seen[user.id] = []
    if form.search.data == '' or form.search.data is None:
        discover = get_news_feed(user, start=0, explore=True)
        return render_template('explore.html', user=user, form=form, discover=discover)
    search_discover = Posts.query.filter((and_(Posts.privacy == 'public')), Posts.post_content.like("%{}%".format(form.search.data))).order_by(desc('timestamp')).limit(50).all()
    return render_template('explore.html', user=user, form=form, discover=search_discover)


@app.route('/search', methods=['POST', 'GET'])
@login_required
def search():
    form = SearchForm()
    user = current_user
    searchname = form.search.data
    if searchname == '' or searchname == ' ' or searchname is None:
        return render_template('search.html', user_results=[], user=user, form=form)
    user_results = Users.query.filter(or_(Users.firstname.like("%{}%".format(searchname)), Users.lastname.like("%{}%".format(searchname)), Users.username.like("%{}%".format(searchname)), Users.email.like("%{}%".format(searchname)))).all()
    return render_template('search.html', user_results=user_results, user=user, form=form)


# *******JSON PROCESSORS************#
@app.route('/processor', methods=['POST'])
@login_required
def processor():
    user = current_user
    if request.method == 'POST':
        received = request.form
        print(received)
        if received:
            action = received['action']
            try:  # friend/searchinteract
                friend = int(received['friend'])
                section = received['section']
            except Exception:
                try:  # postsinteract
                    post = int(received['post'])
                    section = received['section']
                except Exception:
                    try:  # noticeinteract
                        search = int(received['search'])
                        section = received['section']
                    except Exception:
                        try:  # check--seen--delete
                            note = int(received['note'])
                            section = received['section']
                        except Exception:  # infinityscroll
                            try:
                                start = int(received['start'])
                                friend = received['friend']
                            except Exception:  # timeline
                                try:
                                    post = int(received['post'])
                                    content = received['comment']
                                except Exception:
                                    try:
                                        post = int(received['post'])
                                    except Exception:
                                        try:
                                            start = int(received['start'])
                                            friend = int(received['friend'])
                                        except Exception:
                                            try:
                                                start = int(received['start'])
                                            except Exception:
                                                try:
                                                    friend = int(received['friend'])
                                                except Exception:
                                                    media = received['media']
            if action == 'addfriend':
                do_before(user, friend=friend, action='addfriend')
                process = add_friend(user, friend)
                if process == 'done':
                    return jsonify({'result': 'friendrequestsent', 'section': section, 'friend': friend})
                else:
                    return jsonify({'result': 'failed'})
            elif action == 'unfriend' or action == 'friendrequestsent':
                do_before(user, friend=friend, action='unfriend')
                process = unfriend(user, friend)
                if process == 'done':
                    return jsonify({'result': 'unfriended', 'section': section, 'friend': friend})
                else:
                    return jsonify({'result': 'failed'})
            elif action == 'accept':
                do_before(user, friend=friend, action='accept')
                process = accept(user, friend)
                do_before(user, friend=friend, action='deleteafter')
                if process == 'done':
                    return jsonify({'result': 'accepted', 'section': section})
                else:
                    return jsonify({'result': 'failed', 'section': section})
            elif action == 'decline':
                do_before(user, friend=friend, action='decline')
                process = decline(user, friend)
                do_before(user, friend=friend, action='deleteafter')
                if process == 'done':
                    return jsonify({'result': 'declined', 'section': section})
                else:
                    return jsonify({'result': 'failed', 'section': section})
            elif action == 'follow':
                do_before(user, friend=friend, action='follow')
                process = follow(user, friend)
                if process == 'done':
                    return jsonify({'result': 'followed', 'section': section, 'friend': friend})
                else:
                    return jsonify({'result': 'failed'})
            elif action == 'unfollow':
                do_before(user, friend=friend, action='unfollow')
                process = unfollow(user, friend)
                if process == 'done':
                    return jsonify({'result': 'unfollowed', 'section': section, 'friend': friend})
                else:
                    return jsonify({'result': 'failed'})
            elif action == 'like':
                process = like(user, post)
                count = get_likes(post, count=True)
                if process == 'done':
                    return jsonify({'result': 'liked', 'countlikes': count, 'postid': post, 'section': section})
                else:
                    return jsonify({'result': 'failed'})
            elif action == 'unlike':
                process = unlike(user, post)
                count = get_likes(post, count=True)
                if process == 'done':
                    return jsonify({'result': 'unliked', 'countlikes': count, 'postid': post, 'section': section})
                else:
                    return jsonify({'result': 'failed'})
            elif action == 'delete':
                process = deleteIt(user, postid=post)
                if process == 'done':
                    return jsonify({'result': 'deleted', 'section': section})
                else:
                    return jsonify({'result': 'failed'})
            elif action == 'c_like':
                process = like(user, post, comment=True)
                count = get_likes(post, count=True, comment=True)
                if process == 'done':
                    return jsonify({'result': 'c_liked', 'countlikes': count, 'postid': post, 'section': section})
                else:
                    return jsonify({'result': 'failed'})
            elif action == 'c_unlike':
                process = unlike(user, post, comment=True)
                count = get_likes(post, count=True, comment=True)
                if process == 'done':
                    return jsonify({'result': 'c_unliked', 'countlikes': count, 'postid': post, 'section': section})
                else:
                    return jsonify({'result': 'failed'})
            elif action == 'c_delete':
                process = deleteIt(user, commentid=post)
                if process == 'done':
                    return jsonify({'result': 'deleted', 'section': section})
                else:
                    return jsonify({'result': 'failed'})
            elif action == 'deletenote':
                do_before(user, friend=None, noteid=note, action='deletenote')
                process = deleteIt(user, noteid=note)
                if process == 'done':
                    return jsonify({'result': 'deleted', 'section': 'delete{}'.format(note)})
                else:
                    return jsonify({'result': 'failed', 'section': 'delete{}'.format(note)})
            elif action == 'seen':
                process = seen(noteid=note)
                if process == 'done':
                    return jsonify({'result': 'seen', 'note': note, 'section': section})
                else:
                    return jsonify({'result': 'failed', 'section': 'delete{}'.format(note)})
            elif action == 'previous_messages':
                process = get_messages(user, friend, start)
                if process != 'failed':
                    return jsonify({'result': render_template('previous-messages.html', user=user, messages=process)})
                else:
                    return jsonify({'result': 'failed'})
            elif action == 'getcomments':
                process = get_comments(postid=post)
                if process != 'failed':
                    return jsonify({'result': render_template('comments.html', user=user, comments=process), 'postid': post, 'count': get_comments(int(post), count=True)})
                else:
                    return jsonify({'result': 'failed', 'postid': post})
            elif action == 'postcomments':
                process = comment(user, post, content)
                if process != 'failed':
                    return jsonify({'result': content, 'postid': str(post), 'username': user.username})
                else:
                    return jsonify({'result': 'failed'})
            elif action == 'loadmorepost':
                process = get_news_feed(user, start)
                if process == 'failed':
                    return jsonify({'result': 'failed'})
                else:
                    return jsonify({'result': render_template('loadmore.html', user=user, streams=process)})
            elif action == 'loadgallery':
                process = get_gallery(user, get=media)
                if process == 'failed':
                    return jsonify({'result': 'failed'})
                else:
                    return jsonify({'result': render_template('loadgallery.html', gallery_items=process)})
            elif action == 'exploremore':
                process = get_news_feed(user, start, explore=True)
                if process == 'failed':
                    return jsonify({'result': 'failed'})
                else:
                    return jsonify({'result': render_template('exploremore.html', user=user, streams=process)})
            elif action == 'loaduserpost':
                if friend == 'None':
                    uzer = user
                else:
                    uzer = get_user(userid=int(friend))
                process = get_news_feed(uzer, start, only=True)
                if process == 'failed':
                    return jsonify({'result': 'failed'})
                else:
                    return jsonify({'result': render_template('loadmore.html', user=user, streams=process)})
            else:
                return jsonify({'result': 'failed'})
        return jsonify({'result': 'failed'})
    abort(404)


@app.route('/processor/apps', methods=['POST'])
def apps_processor():
    user = current_user
    if request.method == 'POST':
        received = request.form
        print(received)
        if received:
            action = received['action']
            app_name = received['app']
            this = received['by']

            if action == 'search':
                process = apps_func(app_name, action=action, this=this)
                if process == 'failed':
                    return({'result': 'failed'})
                else:
                    return jsonify({'result': render_template('slide-results.html', results=process)})
            elif action == 'delete':
                process = apps_func(app_name, action=action, this=this, user=user)
                if process == 'done':
                    return jsonify({'result': 'deleted'})
                else:
                    return({'result': 'failed'})
            elif action == 'update':
                process = apps_func(app_name, action=action, this=this, user=user)
                if process == 'done':
                    return jsonify({'result': 'updated'})
                else:
                    return({'result': 'failed'})
            else:
                pass
        

# ********PASSWORD CHANGE ROUTES**********#

@app.route('/change_password', methods=['POST', 'GET'])
@login_required
def change_password():
    form = CResetForm()
    if request.method == 'POST':
        user = current_user
        password = user.password
        if form.validate_on_submit():
            if check_password_hash(password, form.old_password.data):
                user.password = generate_password_hash(form.new_password.data, method='sha256')
                db.session.add(user)
                db.session.commit()
                flash("Your password has been succesfully updated", 'success')
                return redirect(url_for('profile', username=user.username))
            flash("password's don't match", 'error')
            return redirect(url_for('change_password'))
        return redirect(url_for('change_password'))
    return render_template('change.html', form=form)


@app.route('/forgot', methods=['POST', 'GET'])
def recover_we():
    form = EResetForm()
    if request.method == 'POST':
        user = get_user(email=form.user_email.data)
        if form.validate_on_submit():
            if user:
                if user.confirmed_email == 'true':
                    email = form.user_email.data
                    token = s.dumps(email, salt='forgot.recovery@key')
                    msg = Message('Password Reset', sender='chatapp.gh@gamil.com', recipients=[email])
                    link = (url_for('reset', token=token, _external=True))
                    msg.body = "Click the link {} to reset your password".format(link)
                    msg.html = render_template('mail/recovery.html', user=user, link=link)
                    mail.send(msg)
                    flash('Email Sent, check your inbox and follow the steps', 'success')
                    return redirect(url_for('login'))
                flash("Your email is not confirmed, please confirm to continue", 'error')
                return redirect(url_for('verify'))
            flash('Email not recognized', 'error')
            return redirect(url_for('recover_we'))
        flash('Validation Email not recognized', 'error')
        return redirect(url_for('recover_we'))
    return render_template('forgot-e.html', form=form)


@app.route('/forgot/phone', methods=['POST', 'GET'])
def recover_wp():
    form = PResetForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            user = get_user(phone=form.user_phone.data)
            if user:
                if user.confirmed_phone == 'true':
                    phone = form.user_phone.data
                    token = s.dumps(phone, salt='forgot.recovery@key')
                    link = (url_for('reset', token=token, _external=True))
                    msg = ("ChatAPP\n\n Reset Password \nClick the link\n {} \n to reset your password\n\nSender : Chingy@Chatapp.gh".format(link))
                    twilio_send(phone, msg)
                    flash('Message Sent, check your inbox and follow the steps', 'success')
                    return redirect(url_for('login'))
                flash("your phone number is not confirmed, please confirm to continue", 'error')
                return redirect(url_for('verify'))
            flash('phone number not recognized', 'error')
            return redirect(url_for('recover_wp'))
        flash('phone number not recognized', 'error')
        return redirect(url_for('recover_wp'))
    return render_template('forgot-p.html', form=form)


@app.route('/reset_password/<token>', methods=['POST', 'GET'])
def reset(token):
    form = FResetForm()
    try:
        data = s.loads(token, salt='forgot.recovery@key', max_age=600)
    except Exception:
        flash("You can't access this page, Invalid token!", 'error')
        return redirect(url_for('recover_we'))

    e_user = get_user(email=data)
    p_user = get_user(phone=data)
    if e_user or p_user:
        if request.method == 'POST':
            if form.validate_on_submit():
                try:
                    if e_user:
                        e_user.password = generate_password_hash(form.new_password.data, method='sha256')
                        db.session.add(e_user)
                        db.session.commit()
                        flash('Password changed successfully', 'success')
                        return redirect(url_for('login'))
                    p_user.password = generate_password_hash(form.new_password.data, method='sha256')
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
            return render_template('reset.html', form=form, token=token)
        return render_template('reset.html', form=form, token=token)
    flash("you can't access this page, invalid token!", 'error')
    return redirect(url_for('recover_we'))


# **********SETTINGS AND HELP*************#
@app.route('/settings', methods=['POST', 'GET'])
@login_required
def settings():
    user = current_user
    form = SettingsForm()
    return render_template("settings.html", form=form, user=user)


@app.route('/help', methods=['POST', 'GET'])
@login_required
def _help():
    user = current_user
    form = HelpForm()
    addform = AddHelpForm()
    if form.help_search.data == '' or form.help_search.data == ' ' or form.help_search.data is None:
        return render_template("help.html", form=form, addform=addform, user=user, results=[])
    help_results = Help.query.filter(or_(Help.help_topic.like("%{}%".format(form.help_search.data)), Help.help_content.like("%{}%".format(form.help_search.data)))).all()
    return render_template("help.html", form=form, addform=addform, user=user, results=help_results)


@app.route('/add_help', methods=['POST'])
@login_required
def add_help():
    user = current_user
    addform = AddHelpForm()
    if addform.validate_on_submit():
        if user.user_status == 'goduser':
            new_help_note = Help(help_topic=addform.helptopic.data, help_content=addform.helpcontent.data)
            db.session.add(new_help_note)
            db.session.commit()
            return redirect(url_for('_help'))




@app.route('/offline_help', methods=['POST', 'GET'])
def offline_help():
    form = HelpForm()
    if form.help_search.data == '' or form.help_search.data == ' ' or form.help_search.data is None:
        return render_template("offline-help.html", form=form, results=[])
    help_results = Help.query.filter(or_(Help.help_topic.like("%{}%".format(form.help_search.data)), Help.help_content.like("%{}%".format(form.help_search.data))))
    return render_template("offline-help.html", form=form, results=help_results)


@app.route('/myaccount', methods=['POST', 'GET'])
@login_required
def myaccount():
    user = current_user
    return render_template("myaccount.html", user=user)


# ********VERIFICATION ROUTES****
@app.route('/verify', methods=['POST', 'GET'])
def verify():
    form = ConfirmForm()
    data = form.input.data
    if form.validate_on_submit():
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
    return render_template('verify.html', form=form)


@app.route('/send_welcome')
def send_welcome_message(email):
    user = current_user
    msg = Message('Welcome to ChatAPP', sender='chatapp@techupstudio.com', recipients=[email])
    msg.body = "Welcome to Chatapp, The best social network for Universities an colleges, Learn, share and have fun. "
    msg.html = render_template('mail/welcome.html', user=user)
    mail.send(msg)


@app.route('/sendlink/<email>')
def send_confirmation_email(email):
    user = get_user(email=email)
    if user:
        if user.confirmed_email != 'true':
            token = s.dumps(email, salt='confirm-ekey')
            msg = Message('Ccfirm Email', sender='chatapp@techupstudio.com', recipients=[email])
            link = url_for('confirm_email', token=token, _external=True)
            msg.body = "Click the link {} to confirm your account".format(link)
            msg.html = render_template('mail/confirm-account', user=user, link=link)
            mail.send(msg)
            return redirect(url_for('login'))
        flash('User already verified', 'error')
        return redirect(url_for('profile', username=user.username))
    flash('Email not registered!', 'error')
    return redirect(url_for('verify'))


@app.route('/send_link/<phone>')
def send_confirmation_link(phone):
    user = get_user(phone=phone)
    if user:
        if user.confirmed_phone != 'true':
            token = s.dumps(phone, salt='confirm-pkey')
            link = url_for('confirm_phone', token=token, _external=True)
            msg = ("ChatAPP\n\n Confirm Number \nClick the link\n {} \n to confirm your account\n\nSender : Chingy@Chatapp.gh".format(link))
            twilio_send(phone, msg)
            return redirect(url_for('login'))
        flash('User already verified', 'error')
        return redirect(url_for('profile', username=user.username))
    flash('Number not registered!', 'error')
    return redirect(url_for('verify'))


@app.route('/confirm_email/<token>')
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
            flash("Sorry '{}', The confimation link has expired, go to your profile and request for a new confirmation link".format(user.username), 'error')
            return redirect(url_for('verify'))
        elif BadSignature:
            flash("The link is invalid, please go to your profile and request for a confirmation link", 'error')
            return redirect(url_for('settings'))
        else:
            flash("Cannot recognize link, please login and request for an conformation link", 'error')
            return redirect(url_for('verify'))


@app.route('/confirm_phone/<token>', methods=['POST'])
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
            flash("The confimation link has expired, go to your profile and request for a new confirmation link", 'error')
            return redirect(url_for('verify'))
        elif BadSignature:
            flash("The link is invalid, please go to your profile and request for a confirmation link", 'error')
            return redirect(url_for('settings'))
        else:
            flash("Cannot recognize link, please login and request for an conformation link", 'error')
            return redirect(url_for('verify'))


# **********LOGOUT AND ERROR HANDLERS**#

@app.errorhandler(404)
def lost(e):
    form = HelpForm()
    return render_template("404.html", form=form), 404


@app.errorhandler(403)
def forbidden(e):
    form = HelpForm()
    return render_template("403.html", form=form), 403


@app.errorhandler(400)
def bad_request(e):
    form = HelpForm()
    return render_template("400.html", form=form), 400


@app.errorhandler(405)
def restricted(e):
    form = HelpForm()
    return render_template("405.html", form=form), 405


@app.errorhandler(500)
def unavailable(e):
    form = HelpForm()
    return render_template("500.html", form=form), 500


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("you logged out", 'success')
    return redirect(url_for('home'))


if __name__ == "__main__":
    # Build a sample db on the fly, if one does not exist yet.
    connect_to_db(app)
    socketio.run(app, debug=True, host="10.0.143.142", port=80)