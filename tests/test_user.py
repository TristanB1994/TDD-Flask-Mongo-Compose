from application.models import User


def test__create_user(database):
    email = "random.email@server.com"
    user = User(email=email)
    user.save()

    user = User.objects().first()

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

    assert updated_user.email == new_email

def test__delete_user(database):
    email = "random.email@server.com"
    user = User(email=email)
    user.save()

    user = User.objects(email=email).first()

    user.delete()

    assert User.objects(email=email).first() == None