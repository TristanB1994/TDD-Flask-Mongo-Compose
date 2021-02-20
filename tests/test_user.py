from application.models import User


def test__create_user(database):

    email = "random.email@server.com"
    user = User(email=email)
    user.save()

    user = User.objects(email=email).first()

    assert user.email == email

def test__update_user(database):

    email = "random.email@server.com"
    user = User(email=email)
    user.save()

    pulled_user = User.objects(email=email).first()
    new_email = "not.random.email@server.com"
    pulled_user.email = new_email
    pulled_user.save()

    updated_user = User.objects().first()

    assert updated_user._get_email() == new_email

def test__delete_user(database):

    email = "random.email@server.com"
    user = User(email=email)
    user.save()

    user = User.objects(email=email).first()

    user.delete()

    assert User.objects(email=email).first() == None

# def test__fill_user_attr(database, load_admin_data):

#     user = User(**load_admin_data)
#     user.save()

#     fields = { x:False for x in load_admin_data.keys() }

#     for k,v in user._data.items():
#         if ( k in fields.keys() and load_admin_data[k] == v ):
#             if v == load_admin_data[k]:
#                 fields[k] = True

#     for k,v in fields.items():
#         assert fields[k] == True

####################################################################

# def test__user_str(load_admin_data):

#     user = User(**load_admin_data)
#     user_username = user.username

#     assert user.__str__() == f"<User: {user_username}"