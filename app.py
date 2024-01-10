from flask import Flask, render_template, url_for, redirect, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import shortener

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///date_base.db'
db = SQLAlchemy(app)

shortened_urls = {}

class Date_Base(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(50), nullable=False)
    full_url = db.Column(db.String, nullable=False)
    short_url = db.Column(db.String(), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Date_Base %r>' % self.id


@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        long_url = request.form['long_url']
        short_url = shortener.generate_short_url()
        while short_url in shortened_urls:
            short_url = shortener.generate_short_url()

        shortened_urls[short_url] = long_url

        return render_template('short_url.html', short_url = short_url)
    return render_template('index.html')


@app.route('/<short_url>')
def redirect_url(short_url):
    long_url = shortened_urls.get(short_url)
    if long_url:
        return redirect(long_url)
    else:
        return 'Url not found'

if __name__ == '__main__':
    app.run(debug=True)