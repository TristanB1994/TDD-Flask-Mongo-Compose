from flask import Blueprint, render_template
from application.models import User

front_blueprint = Blueprint('front_blueprint', __name__)

@front_blueprint.route("/")
def hello_world():
    return render_template('index.html')

@front_blueprint.route("/users")
def users():
    num_users = User.objects().count()
    users = [ x for x in User.objects() ]
    print("=========="*4)
    print(f"Users: {users}")
    print("=========="*4)
    return render_template('users_count.html', users=users)
