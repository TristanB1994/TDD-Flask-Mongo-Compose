from flask_admin import Admin, AdminIndexView
from flask_security import Security, current_user
from flask_debugtoolbar import DebugToolbarExtension
from flask import redirect, url_for
from itsdangerous import URLSafeSerializer
from application.models import user_datastore

# Index View Class
class MyAdminIndexView(AdminIndexView):

    def is_accessible(self):
        # return current_user.is_authenticated
        # return (current_user.is_active and current_user.is_authenticated)
        return current_user.is_authenticated

    def _handle_view(self, name):
        if not self.is_accessible():
            return redirect(url_for('security.login'))

# Flask-Admin Class
admin = Admin(index_view=MyAdminIndexView(), template_mode='bootstrap3')

# Flask-User UserClass
# user_manager = UserManager

# # Create Serializer
serializer = URLSafeSerializer

# Flask-Debugtoolbar
debug_toolbar = DebugToolbarExtension

# Flask-Security Classes
# user_datastore = MongoEngineUserDatastore
# security = Security(datastore=user_datastore)
# security = Security(user_datastore)
security = Security()

# print(f"security dir: {dir(security)}")