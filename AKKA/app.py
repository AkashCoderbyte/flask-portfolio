from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import os
from extensions import db   # import db from the new file
from models import Message   # you can safely import now

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET', 'dev-secret')

# Database configuration
basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, 'portfolio.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize db with app
db.init_app(app)

# Example projects
PROJECTS = [
    {"title": "Calculator (Python)", "summary": "A CLI calculator app", "tech": "Python"},
    {"title": "Student Management System", "summary": "CRUD app using MySQL", "tech": "Python, MySQL"},
    {"title": "Portfolio Website", "summary": "Built with Flask", "tech": "Flask, HTML, CSS"},
]

with app.app_context():
    db.create_all()


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/projects')
def projects():
    return render_template('projects.html', projects=PROJECTS)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message_text = request.form.get('message')

        if not name or not email or not message_text:
            flash("Please fill all fields.", "error")
            return redirect(url_for('contact'))

        msg = Message(name=name, email=email, message=message_text)
        db.session.add(msg)
        db.session.commit()

        flash("Thanks! Your message has been sent.", "success")
        return redirect(url_for('contact'))

    return render_template('contact.html')


if __name__ == '__main__':
    app.run(debug=True)
