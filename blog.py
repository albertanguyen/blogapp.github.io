from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, ValidationError
from wtforms.validators import EqualTo, Length, DataRequired, Email
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, LoginManager, UserMixin



app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/blog.db'
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = "VVSECRET"

# establise connection between app and other libraries 
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id) # Fetch the user from the database

# -----------------------
# Define model here
# -----------------------
class User(db.Model):
    """ 
    Class Argument: Inherit the baseclasss db.Model
    Private vars: 
        __id 
        __username
        __email
        __password
    (Public) functions: 
        __repr__ (representation)
        set_password
        check_password 
    Note: Any changes happens with the db,
        sync the db and run the changes by the following commands (type in terminal):
        python <your app>.py db init
        $ python <your app>.py db migrate
        $ python <your app>.py db upgrade
    """
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

    # def add_column():
    #     """append new column"""
    #     pass

    def set_password(self, password):
        self.__password = generate_password_hash(password)



    def check_password(self, password):
        return check_password_hash(self.__password, password)


db.create_all()

#---------------------
# Define forms here
#---------------------
class Registration(FlaskForm):
    """
    Class Argument: Inherit classbase FlaskForm
    Local vars: 
        username
        email
        password
        pass
        confirm
        submit
    (Public) functions:
        validate_username 
        validate_email   
    """
    username = StringField("User Name", validators=[DataRequired(), Length(min=3, max=79)])
    email = StringField("Email", validators=[DataRequired(), Length(max=254)])
    password = PasswordField("Password", validators=[DataRequired(), EqualTo('pass_confirm')])
    pass_confirm = PasswordField("Confirm Password", validators=[DataRequired()])
    submit = SubmitField("Register")

    # def __init__(self, username, email, password, pass_confirm, submit, *args):
    #     self.__username = username
    #     self.__email = email
    #     self.__password =password
    #     self.__pass_confirm = pass_confirm
    #     self.__submit = submit

    def validate_username(self, field):
        """
        Purpose: cross-check with the database from of User class 
        Inherited function: validate_<field>
        params:
        field:  
        Note:
        query.filter_by (or query.filter) use column name to communicat w/ the db

        """
        if User.query.filter_by(_User__username = field.data).first():
            raise ValidationError('You already registered with this username')

    def validate_email(self, field):
        if User.query.filter_by(_User__email = field.data).first():
            raise ValidationError('You already used this email to register')


class LoginForm(FlaskForm):
    """ 
    Class Argument: Inherit classbase FlaskForm
    How to log in either username of email and exclude confirm password field? 
        Local vars: 
        username
        email
        password
        pass
        confirm
        submit
    (Public) functions:

    """
    email = StringField("Email", validators=[DataRequired(), Length(max=254)])
    password = PasswordField("Password", validators=[DataRequired(), EqualTo('pass_confirm')])
    pass_confirm = PasswordField("Confirm Password", validators=[DataRequired()])
    submit = SubmitField("Register")

    def validate_email(self, field):
        if User.query.filter_by(_User__email = field.data).first():
            raise ValidationError('Please make sure you type the correct email used to register for this blog')


# -----------------------
# Define route here
# -----------------------

@app.route('/') # Default at: https://localhost:5000
def index():
    text = 'Howdy!'
    return render_template('index.html', text = text)

@app.route('/list_user')
def list_user():
    users = User.query.all()
    return render_template('list_user.html', users = users)

@app.route('/register', methods = ['GET', 'POST'])
def register_user():
    form = Registration()
    if form.validate_on_submit():
        new_user = User(username = form.username.data,
                    email = form.email.data)

        new_user.set_password(form.password.data)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for("Message"))
    return render_template('register.html', form = form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        log_user = User.query.filter_by(email=form.email.data).first()
        if log_user is None:
            return redirect(url_for('register_user'))

        if not log_user.check_password(form.password.data):
            return render_template('login.html', form=form)

        login_user(log_user)

        return redirect(url_for('welcome'))
    return render_template('login.html', form=form)



@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/message')
def Message():
    return "Thanks for your registration"


if __name__ == '__main__':
    app.run()