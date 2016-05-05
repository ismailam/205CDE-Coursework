from flask import Flask, render_template, request, flash, session, url_for, redirect, g
import os
from flask_bootstrap import Bootstrap
from functools import wraps
from flask.ext.mail import Message, Mail
from flask_wtf import Form
from wtforms import StringField, TextField, TextAreaField, IntegerField, SubmitField, validators, ValidationError, PasswordField
from wtforms.validators import DataRequired, Length

#from flask.ext.sqlalchemy import SQLAlchemy
import urllib
import sqlite3

mail = Mail()

app = Flask(__name__)

 #config
app.secret_key = 'my precious'
app.database = 'sample.db'
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USERNAME"] = 'ArtficialHeta@gmail.com'
app.config["MAIL_PASSWORD"] = '38055322Abba.'

#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Heta.db'
Bootstrap(app)
mail.init_app(app)

#db = SQLAlchemy(app)


class signUpForm(Form):
    firstName = StringField('First Name:', validators=[DataRequired()])
    lastName = StringField('Last Name:', validators=[DataRequired()])
    email = TextField("Email",  [validators.Required("Please enter your email address."), validators.Email("Please enter your email address.")])
    password = PasswordField('Password', [validators.Required("Please enter a password.")])
    submit = SubmitField("Create account")

class ContactForm(Form):
    name = TextField("Name",  [validators.Required("Please enter your name.")])
    email = TextField("Email",  [validators.Required("Please enter your email address."), validators.Email("Please enter your email address.")])
    subject = TextField("Subject",  [validators.Required("Please enter a subject.")])
    message = TextAreaField("Message",  [validators.Required("Please enter a message.")])
    submit = SubmitField("Send")



# signup required decorator
def signup_required(f):
  @wraps(f)
  def wrap(*args, **kwargs):
    if 'signUp' in session:
      return f(*args, **kwargs)
    else:
      flash('You need to register first.')
      return redirect(url_for('signup'))
  return wrap


@app.route('/')
def home():
  return render_template('bar.html')

@app.route('/ourProject')
def ourProject():
  return render_template('hetaProject.html')

@app.route('/received')
def received():
    return render_template('mailr.html', success=True)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
  form = ContactForm()

  if request.method == 'POST':
    if form.validate() == False:
      flash('All fields are required.')
      return render_template('mailcontact.html', form=form)

    else:
      msg = Message(form.subject.data, sender='ArtficialHeta@gmail.com', recipients=['kwais3000@gmail.com'])
      msg.body = """
      From: %s <%s>
      %s
      """ % (form.name.data, form.email.data, form.message.data)
      mail.send(msg)

      return redirect(url_for('received'))

  elif request.method == 'GET':
    return render_template('mailcontact.html', form=form)
  




@app.route('/welcome')
@signup_required
def welcome():
    return render_template('index.html')

    

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = signUpForm()
    if request.method == 'POST':
        firstName = form.firstName.data
        lastName = form.lastName.data
        email = form.email.data
        password = form.password.data

        g.db = connect_db()
        cur = g.db.execute("INSERT INTO user (firstName, lastName, email, password)VALUES (?,?,?,?)", (firstName, lastName, email, password))
        g.db.commit()
        g.db.close()
        return redirect(url_for('welcome'))
    else:
      session['signUp'] = True
    return render_template('form_wtf.html', form=form)

@app.route('/donate')
def donate():
  return redirect('https://www.gofundme.com/22dybrw')

@app.route('/support')
def support():
  return redirect('https://www.gofundme.com/22dybrw')
  

# connect to database
def connect_db():
      return sqlite3.connect('sample.db')


if __name__ == '__main__':
    app.run(port=8080, host='0.0.0.0', debug=True)











