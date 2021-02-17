from flask_admin import Admin, AdminIndexView
from flask_user import UserManager, current_user
from itsdangerous import URLSafeSerializer

# Index View Class
class MyAdminIndexView(AdminIndexView):

    def is_accessible(self):
        return current_user.is_authenticated

# Flask-Admin Class
admin = Admin(index_view=MyAdminIndexView(), template_mode='bootstrap3')

# Flask-User UserClass
user_manager = UserManager

# # Create Serializer
serializer = URLSafeSerializer