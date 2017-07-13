from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:password@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'y337kGcys&zP3B'


def blank(text):
    if text == '':
        return True

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(500))

    def __init__(self, title, body):
        self.title = title
        self.body = body


@app.route('/blog', methods=['POST', 'GET'])
def blog_listings():
    '''Display all blogs in the database, or just a specific post if an ID is passed in the GET'''

    posts = Blog.query.all()

    if request.args.get('id'):
        post_id = request.args.get('id')
        post = Blog.query.filter_by(id=post_id).first()
        return render_template('blogpage.html', post=post)

    return render_template('blog.html', posts=posts)


@app.route('/newpost', methods=['POST', 'GET'])
def newpost():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        if not blank(body) and not blank(title):
            new_post = Blog(title, body)
            db.session.add(new_post)
            db.session.commit()
            return redirect('/blog')
        else:
            flash('Looks like you forgot a title or body for your post!', 'error')
            return render_template("newpost.html")
    else:
        return render_template('newpost.html')



if __name__ == '__main__':
    app.run()
