from datetime import datetime

from flask import Flask, render_template, url_for, redirect, request, flash
from flask_login import LoginManager, login_user, logout_user, current_user,login_required
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_migrate import Migrate
from forms import LoginForm, RegistrationForm
import shortener
from sqlalchemy import MetaData

app = Flask(__name__)
app.config.from_object('config')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///list.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)
db = SQLAlchemy(app,metadata=metadata)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
migrate = Migrate(app, db)



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


shortened_urls = {}


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_url = db.Column(db.String, nullable=False)
    short_url = db.Column(db.String, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Article %r>' % self.id


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password = db.Column(db.String(128))
    role = db.Column(db.String(10), index=True)



    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)


@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        full_url = request.form['full_url']
        short_url = shortener.generate_short_url()
        while short_url in shortened_urls:
            short_url = shortener.generate_short_url()
        shortened_urls[short_url] = full_url
        if current_user.is_authenticated:
            article = Article(full_url=full_url, short_url=short_url,user_id=current_user.id)
            try:
                db.session.add(article)
                db.session.commit()
                return redirect('short_url')
            except:
                return 'При преобразовании возникла проблема'
        flash('Для просмотра истории создания ваших ссылок необходимо войти или зарегистрироваться')
        return render_template('nonreg.html',full_url=full_url,short_url=short_url)
    return render_template('index.html')


@app.route('/short_url')
@login_required
def short_url():
    #article = Article.query.order_by(Article.date).all()
    res = db.session.query(Article,User).join(Article, User.id == Article.user_id).all()
    return render_template('short_url.html', res=res)


@app.route('/login')
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    title = "Авторизация"
    login_form = LoginForm()
    return render_template('login.html', page_title=title, form=login_form)


@app.route('/process-login', methods=['POST'])
def process_login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('Вы вошли на сайт')
            return redirect(url_for('index'))
    flash('Неправильное имя пользователя или пароль')
    return redirect(url_for('login'))


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Вы успешно вышли')
    return redirect(url_for('index'))

@app.route('/register')
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    title = "Регистрация"
    return render_template('registration.html',page_title=title, form=form)


@app.route('/process-reg', methods=['POST'])
def process_reg():
    form = RegistrationForm()
    if form.validate_on_submit():
        new_user = User(username=form.username.data,role='user')
        new_user.set_password(form.password.data)
        db.session.add(new_user)
        db.session.commit()
        flash('Вы успешно зарегистрировались!')
        return redirect(url_for('login'))
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash('Ошибка в поле "{}": - {}'.format(
                    getattr(form, field).label.text,
                    error
                ))
        return redirect(url_for('user.register'))


@app.route('/<short_url>')
def redirect_url(short_url):
    try:
        f = Article.query.filter_by(short_url=short_url).one()
        if f.full_url:
            return redirect(f.full_url)
    except:
        return 'Url not found'


if __name__ == '__main__':
    with app.app_context():  # <--- without these two lines,
        db.create_all()  # <--- we get the OperationalError in the title
        app.run(debug=True)
