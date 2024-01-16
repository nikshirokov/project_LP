from flask import Flask, render_template, url_for, redirect, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import shortener


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///list.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

shortened_urls = {}

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    #user_name = db.Column(db.String(50), nullable=False)
    full_url = db.Column(db.String, nullable=False)
    short_url = db.Column(db.String, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Article %r>' % self.id


@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        full_url = request.form['full_url']
        short_url = shortener.generate_short_url()
        while short_url in shortened_urls:
            short_url = shortener.generate_short_url()

        shortened_urls[short_url] = full_url

        article = Article(full_url = full_url, short_url = short_url)

        try:
            db.session.add(article)
            db.session.commit()
            return redirect('short_url')
        except:
            return 'При преобразовании возникла проблема'

    return render_template('index.html')


@app.route('/short_url')
def short_url():
    article = Article.query.order_by(Article.date).all()
    return render_template('short_url.html', article = article)

@app.route('/<short_url>')
def redirect_url(short_url):
    try:
        f = Article.query.filter_by(short_url = short_url).one()
        if f.full_url:
            return redirect(f.full_url)
    except:
            return 'Url not found'


if __name__ == '__main__':
    with app.app_context():         # <--- without these two lines,
        db.create_all()             # <--- we get the OperationalError in the title
        app.run(debug=True)