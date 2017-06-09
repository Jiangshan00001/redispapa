#coding:utf-8
import flask
import flask_login
from flask_login import login_required, logout_user
import wtforms
import flask_wtf
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired
from flask import Blueprint


login_manager = flask_login.LoginManager()
simple_login_blueprint = Blueprint('simple_login_blueprint', __name__,
                                     template_folder='templates')
login_manager.login_view = "simple_login_blueprint.login"

class LoginForm(flask_wtf.FlaskForm):
    username = StringField('user', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    remember = BooleanField("remember password")
    submit = SubmitField()


class LoginUser(flask_login.UserMixin):
    def __init__(self):
        self.id=u''

    def is_active(self):
        return True

    def is_authenticated(self):
        return True
    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            if len(self.id)>0:
                return self.id
        except AttributeError:
            raise NotImplementedError('No `id` attribute - override `get_id`')


    def is_anonymous(self):
        if len(self.id)==0:
            return True
        return False



def is_simple_user_check(username, password):
    print 'is_simple_user_check start'
    try:
        if username=='redissimple' and password=='redissimple':
            return True
    except Exception, e:
        print 'is_simple_user_check error', e
        return False
        pass

@login_manager.user_loader
def load_user(userid):
    #red = Redmine(url, username=username, password=password)
    ll =  LoginUser()
    ll.id=userid
    return ll

@simple_login_blueprint.route("/login", methods=["GET", "POST"])
def login():
    # Here we use a class of some kind to represent and validate our
    # client-side form data. For example, WTForms is a library that will
    # handle this for us, and we use a custom LoginForm to validate.
    form =  LoginForm()
    if form.validate_on_submit():
        # login and validate the user...
        username = form.username.data
        password = form.password.data
        remember = form.remember.data
        if(is_simple_user_check(username, password)):
            user = LoginUser()
            user.id = username
            user.password = password
            user.remember = remember
            flask_login.login_user(user, remember= remember )
            flask.flash("Logged in successfully.")
            return flask.redirect(flask.url_for("index"))

    return flask.render_template("login.html", form=form)



@simple_login_blueprint.route("/logout")
@login_required
def logout():
    flask_login.logout_user()
    return 'logout'

#login_manager.init_app(simple_login_blueprint)


