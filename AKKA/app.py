from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import os
from AKKA.extensions import db, mail   # ✅ imported mail also
from AKKA.models import Message

from flask_mail import Mail, Message as MailMessage

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET', 'dev-secret')

# Database configuration
basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, 'portfolio.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# ✅ Gmail configuration (ADD THIS BELOW)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')   # stored in Render
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')   # stored in Render
app.config['MAIL_DEFAULT_SENDER'] = ('Portfolio Site', os.environ.get('MAIL_USERNAME'))

# Initialize database & mail
db.init_app(app)
mail.init_app(app)

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

        # Save to database
        new_message = Message(name=name, email=email, message=message_text)
        db.session.add(new_message)
        db.session.commit()

        # Try sending email
        try:
            email_msg = MailMessage(   # ✅ use MailMessage
                subject=f"New message from {name}",
                sender=os.environ.get('MAIL_USERNAME'),
                recipients=[os.environ.get('MAIL_USERNAME')],
                body=f"From: {name}\nEmail: {email}\n\nMessage:\n{message_text}"
            )
            mail.send(email_msg)
            flash("Thanks! Your message has been sent successfully.", "success")
        except Exception as e:
            print("Error sending email:", e)
            flash("Something went wrong while sending the email. Please try again later.", "error")

        return redirect(url_for('contact'))

    return render_template('contact.html')


if __name__ == '__main__':
    app.run(debug=True)




