from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, ValidationError
from wtforms.validators import EqualTo, Length, DataRequired, Email
from werkzeug.security import generate_password_hash, check_password_hash

# create app
app = Flask(__name__)

# config app
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/blog.db'
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = "VVSECRET"

# create connection between app and sqlalchemy
# https://flask-sqlalchemy.palletsprojects.com/en/2.x/config/
db = SQLAlchemy(app)

# create connection between app and sqlalchemy and migrate
# need Flask-Migarte to work with Flask and Flask-SQLAlchemy
# Write the data into physical memory 
migrate = Migrate(app, db)

# -----------------------
# Define model here
# After everytime the model is updated, sync model and physical db my running flask upgrade
# -----------------------
class User(db.Model):
    __id = db.Column(db.Integer, primary_key=True)
    __username = db.Column(db.String(80), unique=True, nullable=False)
    __email = db.Column(db.String(255), unique=True, nullable=False)
    __password = db.Column(db.String(256), nullable=False)

    def __init__(self, username, email, password='', *arg):
        self.__username = username
        self.__email = email
        self.__password = password

    def __repr__(self):
        return '<User {}>'.format(self.__username)

    def set_password(self, password):
        self.__password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.__password, password)


db.create_all()

#---------------------
# model ends here
#---------------------

#---------------------
# Define forms here
#---------------------
class Registration(FlaskForm):
    """
    In: Inherite FlaskForm syntax, command to create a form
    Out:
    """
    username = StringField("User Name", validators=[DataRequired(), Length(min=3, max=79)])
    email = StringField("Email", validators=[DataRequired(), Length(max=254)])
    password = PasswordField("Password", validators=[DataRequired(), EqualTo('pass_confirm')])
    pass_confirm = PasswordField("Confirm Password", validators=[DataRequired()])
    submit = SubmitField("Register")

    def validate_username(self, field):
        """
        builtin function: validate_<private var>
        params:
        field:  
        check with input of User class
        out: true?
        """
        if User.query.filter_by(_User__username = field.data).first():
            raise ValidationError('You already registered with this username')

    def validate_email(self, field):
        """

        """
        if User.query.filter_by(_User__email = field.data).first():
            raise ValidationError('You already used this email to register')


class login_Form(FlaskForm):
    """
    In: 
    Out:
    """
    email = StringField("Email", validators=[DataRequired(), Length(max=254)])
    password = PasswordField("Password", validators=[DataRequired(), EqualTo('pass_confirm')])
    pass_confirm = PasswordField("Confirm Password", validators=[DataRequired()])
    submit = SubmitField("Register")

    def validate_email(self, field):
        if User.query.filter_by(_User__username = field.data).first():
            raise ValidationError('Please make sure you type the correct email used to register for this blog')

    

# -----------------------
# Define route here
# -----------------------

@app.route('/') # https://localhost:5000
def index():
    text = 'Howdy!'
    return render_template('index.html', text = text)

@app.route('/user/<username>/<email>')
def add_user(username, email, password="1"):
    """
    get user info and add to database
    """
    new_user = User(username=username, email = email, password = password)

    db.session.add(new_user)
    db.session.commit()

    return "Add new user sucessfully " + username

@app.route('/list_user')
def list_user():
    users = User.query.all()
    return render_template('list_user.html', users = users)

@app.route('/register', methods = ['GET', 'POST'])
def register_user():
    form = Registration()
    if form.validate_on_submit():
        # post method here
        # calculate hash password
        new_user = User(username = form.username.data,
                    email = form.email.data)

        new_user.set_password(form.password.data)
        db.session.add(new_user)
        db.session.commit()
        # get method here

        return redirect(url_for("Message"))
    return render_template('register.html', form = form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = login_Form()
    if form.validate_on_submit():
        log_user = User.query.filter_by(email=form.email.data).first()
        if log_user is None:
            # 'register_user' find the route where it have tha name of this function
            return redirect(url_for('register_user'))

        if not log_user.check_password(form.password.data):
            # handle password is wrong
            return render_template('login.html', form=form)

        # login here
        login_user(log_user)

        return redirect(url_for('welcome'))
    return render_template('login.html', form=form)



@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/welcome')
def welcome():
    return render_template('welcome.html')   

@app.route('/message')
def Message():
    return "Thanks for your registration"


if __name__ == '__main__':
    app.run()