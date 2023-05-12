from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)



class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    date = db.Column(db.String(50), nullable=False)
    steps = db.Column(db.Integer)

    def __repr__(self):
        return '<Article %r>' % self.id


@app.route('/')
@app.route('/home')
def index():
    articles = Article.query.all()
    return render_template("index.html", articles=articles)


@app.route('/posts')
def posts():
    articles = Article.query.all()
    return render_template("posts.html", articles=articles)


@app.route('/posts/<int:id>')
def posts_detail(id):
    article = Article.query.get(id)
    return render_template("post_detail.html", article=article)


@app.route('/posts/<int:id>/delete')
def posts_delete(id):
    article = Article.query.get_or_404(id)

    try:
        db.session.delete(article)
        db.session.commit()
        return redirect('/posts')
    except:
        return "При удалении статьи произошла ошибка"


@app.route('/posts/<int:id>/update', methods=['POST', 'GET'])
def update_article(id):
    article = Article.query.get(id)
    if request.method == 'POST':
        article.title = request.form['title']
        article.date = request.form['date']
        article.steps = request.form['steps']

        try:
            db.session.commit()
            return redirect('/posts')
        except:
            return "При редактировании произошла ошибка"
    else:
        return render_template("post_update.html", article=article)


@app.route('/create-article', methods=['POST', 'GET'])
def create_article():
    if request.method == 'POST':
        title = request.form['title']
        date = request.form['date']
        steps = request.form['steps']

        article = Article(title=title, date=date, steps=steps)

        try:
            db.session.add(article)
            db.session.commit()
            return redirect('/posts')
        except:
            return "Ошибка"
    else:
        return render_template("create-article.html")


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
