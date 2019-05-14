import os
import datetime
from operator import attrgetter

from sqlalchemy.dialects.postgresql import JSONB
from database import Admins, Subscibers, Posts, Gallery, Feedbacks
from database import db, connect_to_db
from flask import Flask, redirect, render_template, url_for, flash, g, jsonify, request, abort
import flask_admin as admins
from flask_admin import Admin, helpers
from flask_admin.base import expose
from flask_admin.contrib import sqla
# from flask_admin.contrib.sqla.view import ModelView
from flask_bootstrap import Bootstrap
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_mail import Mail, Message
from flask_uploads import UploadSet, configure_uploads, extension, patch_request_class, IMAGES, AUDIO, DOCUMENTS
from flask_wtf import FlaskForm
from itsdangerous import URLSafeTimedSerializer, URLSafeSerializer, SignatureExpired, BadSignature
from sqlalchemy.sql.expression import desc, or_, cast, func, and_
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms import StringField, PasswordField, BooleanField, MultipleFileField, form, fields, validators, widgets
from wtforms.validators import InputRequired, Length, Email, ValidationError, EqualTo




app = Flask(__name__)
app.config['SECRET_KEY'] = "iamotc&ifuckingrule@#techup#"
# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:Asdwe111@localhost:5432/blog'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config.from_pyfile('config.cfg')
Bootstrap(app)
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


# ********VALIDILITY FUNCTIONS**********#
def get_user(userid=None, phone=None, email=None, username=None):
    if userid:
        user = Admins.query.filter_by(id=userid).first()
    elif email:
        user = Admins.query.filter_by(email=email).first()
    elif phone:
        user = Admins.query.filter_by(phone=phone).first()
    elif username:
        user = Admins.query.filter_by(username=username).first()
    return user


def user_exists(form, field):
    user = get_user(username=form.username.data)
    if user:
        raise ValidationError('User with this name already exists.')


def email_exists(form, field):
    email = get_user(email=form.email.data)
    if email:
        raise ValidationError('User with this email already exists.')


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

def get_suggestions():
    pass

def send_feedback(name,email, phone, content):
    feedback = Feedbacks(name=name, email=email, phone=phone, content=content, timestamp=datetime.datetime.now())
    # send feedback as email to admins
    db.session.add(feedback)
    db.session.commit()
    return 'done'


def get_feedbacks():
    feedbacks = Feedbacks.query.all()
    return feedbacks


def add_subscriber(email):
    user = get_user(email=email).first()
    if not user:
        new_subscriber = Subscibers(email=email)
        db.session.add(new_subscriber)
        db.session.commit()
        return 'done'
    return 'failed'


def get_post(start):
    count = 0
    index = start
    streams = []
    stream = (Posts.query.filter_by(privacy="public").limit(100).all())[::-1]
    # streamz = sorted(stream, key=attrgetter('timestamp'), reverse=True)
    if stream is None:
        return 'failed'
    else:
        while count != 3:
            try:
                post = stream[index]
                streams.append(post)
                index += 1
                if index >= len(stream):
                    streams.append('reachedMax')
                    return streams
                    break
                else:
                    count += 1
            except Exception:
                return ['reachedMax']
        return streams


def getline(obj):
    if len(obj) > 115:
        return obj[:115]
    return obj


def upload(media, privacy='public', used_as='post'):
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

            if ext.lower() in IMAGES:
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
        new_upload = Gallery(upload_type=filetype, upload_used_as=used_as, upload_path=paths, privacy=privacy, timestamp=datetime.datetime.now())
        db.session.add(new_upload)
        db.session.commit()
        return {'result': 'done', 'path': paths, 'filetype': filetype, 'postname': postname}
    except Exception as e:
        print('error :'+str(e))
        return {'result': 'failed'}



def deleteIt(postid=None, subscriber=None, galleryid=None, path=None):
    if postid:
        post = Posts.query.filter_by(post_id=postid).first()
        if post:
            if (post.post_content['media'][0])['filetype'] != 'None':
                for media in post.post_content['media']:
                    file = Gallery.query.filter(Gallery.upload_path == cast((media['path']), JSONB)).first()
                    if file:
                        deleteIt(galleryid=file.gallery_id)
            db.session.delete(post)
            db.session.commit()
            return 'done'
        return 'failed'
    elif subscriber:
        person = Subscibers.query.filter_by(email=subscriber).first()
        if person:
            db.session.delete(person)
            db.session.commit()
            return 'done'
        return 'failed'
    elif galleryid:
        gallery_item = Gallery.query.filter_by(gallery_id=galleryid).first()
        if gallery_item:
            deleteIt(path=gallery_item.upload_path)
            db.session.delete(gallery_item)
            db.session.commit()
            return 'done'
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


def getDate():
    dt = str(datetime.datetime.now())
    y = dt[:4]
    year = int(y)
    m = dt[5:7]
    month = int(m)
    d = dt[8:10]
    day = int(d)
    h = dt[11:13]
    hour = int(h)
    return datetime.date(day=day,month=month,year=year).strftime('%A %d %B %Y')


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


def get_gallery(get='all'):
    if get == 'all':
        all_gallery = Gallery.query.filter(Gallery.privacy == "public").order_by(desc(Gallery.timestamp)).all()
        return all_gallery
    elif get == 'pics':
        pics_gallery = Gallery.query.filter(Gallery.privacy == "public", Gallery.upload_type == 'photo').order_by(desc(Gallery.timestamp)).all()
        return pics_gallery
    elif get == 'auds':
        pics_gallery = Gallery.query.filter(Gallery.privacy == "public", Gallery.upload_type == 'audio').order_by(desc(Gallery.timestamp)).all()
        return pics_gallery
    elif get == 'vids':
        vids_gallery = Gallery.query.filter(Gallery.privacy == "public", Gallery.upload_type == 'video').order_by(desc(Gallery.timestamp)).all()
        return vids_gallery
    elif get == 'docs':
        vids_gallery = Gallery.query.filter(Gallery.privacy == "public", Gallery.upload_type == 'document').order_by(desc(Gallery.timestamp)).all()
        return vids_gallery
    else:
        return 'failed'



# ******END OF FUNCTIONS*****##
# ******Sending modules in jinjA*****#

app.jinja_env.globals.update(time_ago=time_ago)
app.jinja_env.globals.update(getline=getline)
app.jinja_env.globals.update(len=len)


# ********FORMS************#

class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=5, max=32)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=7, max=80), invalid])
    remember = BooleanField('remember me')

class SearchForm(FlaskForm):
    search = StringField('', validators=[InputRequired(), Length(min=3, max=32)])

class PostForm(FlaskForm):
    headline = StringField('', validators=[InputRequired(), Length(max=3000)])
    body = StringField('', validators=[InputRequired(), Length(max=10000)])

class UploadForm(FlaskForm):
    media = MultipleFileField('', validators=[InputRequired()])

class HelpForm(FlaskForm):
    help_search = StringField('', validators=[InputRequired(), Length(max=200)])

class ResetForm(FlaskForm):
    old_password = PasswordField('Current password', validators=[InputRequired(), Length(max=80)])
    new_password = PasswordField('New password', validators=[InputRequired(), Length(min=7, max=80)])
    confirm_password = PasswordField('Confirm password', validators=[InputRequired(), Length(min=7, max=80), EqualTo('new_password', message="Password's don't match")])

class Recovery(FlaskForm):
    user_email = StringField('Enter your registered email', validators=[InputRequired(), Email(message="Invalid Email"), Length(max=40)])

# ********MAIN ROUTES***********

@app.before_request
def before_request():
    g.user = current_user


@login_manager.user_loader
def load_user(user_id):
    return Admins.query.get(int(user_id))


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
        return db.session.query(Admins).filter_by(username=self.admin_name.data).first_or_404()


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
        return db.session.query(Admins).filter_by(username=str(current_user)).first_or_404()


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
        return db.session.query(Admins).filter_by(username=str(current_user)).first_or_404()

    @expose('/login/', methods=('GET', 'POST'))
    def login_view(self):
        form = AdminLoginForm(request.form)
        if helpers.validate_form_on_submit(form):
            user = form.get_user()
            if user.user_status == 'goduser':
                login_user(user)
            return redirect(url_for('.login_view'))

        if current_user.is_authenticated:
            form = PostForm()
            return redirect(url_for('.index', form=form))
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

admin = Admin(app, "A Lawyer's Diary", index_view=MyAdminIndexView(), base_template='my_master.html')

admin.add_view(MyModelView(Admins, db.session))
admin.add_view(MyModelView(Subscibers, db.session))
admin.add_view(MyModelView(Posts, db.session))
admin.add_view(MyModelView(Gallery, db.session))
admin.add_view(MyModelView(Feedbacks, db.session))

# ****END OF ADMIN ROUTES*******#



@app.route('/', methods=['POST', 'GET'])
@app.route('/home', methods=['POST', 'GET'])
def home():
    form = PostForm()
    posts = get_post(0)
    user = current_user
    return render_template("index.html", admin=user, form=form, posts=posts)

@app.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = get_user(username=form.username.data)
        e_user = get_user(email=form.username.data)
        p_user = get_user(phone=form.username.data)
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                return redirect(url_for('admin.index'))
        elif e_user:
            if check_password_hash(e_user.password, form.password.data):
                login_user(e_user, remember=form.remember.data)
                return redirect(url_for('admin.index'))
        elif p_user:
            if check_password_hash(p_user.password, form.password.data):
                login_user(p_user, remember=form.remember.data)
                return redirect(url_for('admin.index'))
        else:
            flash('Cant find user!, details might be wrong', 'error')
            return render_template("login.html", form=form)
    return render_template("login.html", form=form)

@app.route('/about', methods=['POST', 'GET'])
def about():
    return render_template("about.html")

@app.route('/contact', methods=['POST', 'GET'])
def contact():
    return render_template("contact.html")

@app.route('/post', methods=['POST', 'GET'])
@login_required
def post():
    form = PostForm()
    src = [{'filetype': 'None', 'path': 'None'}]
    privacy = request.form['privacy']
    if request.method == 'POST':
        if 'media' in request.files:
            media = request.files.getlist('media')
            process = upload(media, privacy=privacy, used_as='post')
            if process['result'] == 'done':
                path = process['path']
                type_ =  process['filetype']
                postname = process['postname']
                src = [{'path':path, 'filetype':type_, 'filename': postname}]
            pass
        if form.validate_on_submit():
            new_post = Posts(post_content={'headline': form.headline.data, 'body': form.body.data, 'media': src}, privacy=privacy, timestamp=getDate())
            db.session.add(new_post)
            db.session.commit()
            flash("Post successfull!", "success")
            return redirect(url_for('home'))
        return redirect(url_for("home"))
    abort(400)

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
                    old_media = Gallery.query.filter(Gallery.upload_used_as=='post', Gallery.upload_path == cast(((((edit.post_content)['media'])[0])['path']), JSONB)).first()
                    deleteIt(user, galleryid=old_media.gallery_id)
                    process = upload(media, privacy=privacy, used_as='post')
                    if process['result'] == 'done':
                        path = process['path']
                        type_ =  process['filetype']
                        postname = process['postname']
                        post_media = [{'path':path, 'filetype':type_, 'filename': postname}]
                    pass
                edited_pc = {'post': form.postbox.data, 'media': post_media}
                edit.post_content = edited_pc
                edit.privacy = privacy
                edit.timestamp = getDate()
                edit.edited = 'true'
                db.session.add(edit)
                db.session.commit()
            flash("The post has been succesfully updated", 'success')
            return redirect(url_for('timeline'))
        return render_template('edit-post.html', form=form, old_post=old_post)
    flash("you don't have permission to edit this!!!", 'error')
    return redirect(url_for('/'))


@app.route('/view_post/<postid>', methods=['POST', 'GET'])
def view_post(postid):
    post = Posts.query.filter_by(post_id=postid).first()
    return render_template("view-post.html", post=post)


@app.route('/gallery', methods=['POST', 'GET'])
def gallery():
    gallery_items = get_gallery(get='all')
    return render_template("gallery.html", gallery_items=gallery_items)


@app.route('/search', methods=['POST', 'GET'])
def search():
    form = SearchForm()
    line = form.search.data
    if line == '' or line == ' ' or line is None:
        return render_template('search.html', user_results=[], form=form)
    results = Posts.query.filter(or_(Posts.privacy == "public", Posts.post_content['headline'].contains(line), Posts.post_content['body'].contains(line))).all()
    # results = Posts.query.filter(or_(Posts.privacy == "public", Posts.post_content['headline'].like(line), Posts.post_content['body'].like(line))).all()
    return render_template('search.html', user_results=results, form=form)


# *******JSON PROCESSORS************#

@app.route('/processor', methods=['POST'])
def processor():
    user = current_user
    if request.method == 'POST':
        received = request.form
        print(received)
        if received:
            action = received['action']
            try:  #loadmorepost
                start = int(received['start'])
            except Exception:
                try:  #loadmore gallery
                    media = str(received['media'])
                except Exception:
                    try: #adding subscriber
                        email = str(received['email'])
                    except Exception:
                        try:  # adding feedback
                            name = str(received['name'])
                            phone = str(received['phone'])
                            email = str(received['email'])
                            content = str(received['content'])
                        except Exception:
                            pass
            if action == 'addsubscriber':
                process = add_subscriber(email)
                if process == 'done':
                    return jsonify({'result': 'friendrequestsent', 'section': section, 'friend': friend})
                else:
                    return jsonify({'result': 'failed'})
            elif action == 'sendfeedback':
                process = send_feedback(name, email, phone, content)
                if process != 'failed':
                    return jsonify({'result': 'success'})
                else:
                    return jsonify({'result': 'failed'})
            elif action == 'loadmorepost':
                process = get_post(start)
                if process == ['reachedMax']:
                    return jsonify({'result': 'failed'})
                else:
                    return jsonify({'result': render_template('loadmore.html', streams=process)})
            elif action == 'loadgallery':
                process = get_gallery(get=media)
                if process == 'failed':
                    return jsonify({'result': 'failed'})
                else:
                    return jsonify({'result': render_template('loadgallery.html', gallery_items=process)})
            else:
                return jsonify({'result': 'failed'})
        return jsonify({'result': 'failed'})
    abort(404)


@app.route('/admin_processor', methods=['POST'])
@login_required
def admin_processor():
    user = current_user
    if request.method == 'POST':
        received = request.form
        print(received)
        if received:
            action = str(received['action'])
            try:  # deleting post
                postid = str(received['postid'])
                section = str(received['section'])
            except Exception:
                pass
            if action == 'delete':
                process = deleteIt(postid=postid)
                if process == 'done':
                    return jsonify({'result': 'deleted', 'section': section})
                else:
                    return jsonify({'result': 'failed'})


# ********PASSWORD CHANGE ROUTES**********#

@app.route('/change_adminkey', methods=['POST', 'GET'])
def change_adminkey():
    return render_template("change-adminkey.html")

@app.route('/change_login_details', methods=['POST', 'GET'])
def change_details():
    form = ResetForm()
    if request.method == 'POST':
        user = current_user
        password = user.password
        if form.validate_on_submit():
            if check_password_hash(password, form.old_password.data):
                user.password = generate_password_hash(form.new_password.data, method='sha256')
                db.session.add(user)
                db.session.commit()
                flash("Your password has been succesfully updated", 'success')
                return redirect(url_for('admin_page', username=user.username))
            flash("password's don't match", 'error')
            return redirect(url_for('change_details'))
        return redirect(url_for('change_details'))
    return render_template("change-details.html")


@app.route('/forgot', methods=['POST', 'GET'])
def recover_we():
    form = Recovery()
    if request.method == 'POST':
        user = get_user(email=form.user_email.data)
        if form.validate_on_submit():
            if user:
                if user.confirmed_email == 'true':
                    email = form.user_email.data
                    msg = Message('Password Reset', sender='blog.gh@gamil.com', recipients=[email])
                    key = 'Admin111' #generaterandom admin key...key = randomKey()
                    msg.body = "Click this admin key {} to reset your password".format(key)
                    msg.html = render_template('mail/recovery.html', user=user, link=key)
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
    #starting the app
    connect_to_db(app)
    app.run(debug=True)
    # app.run(debug=True, host="192.168.137.1", port=80)
