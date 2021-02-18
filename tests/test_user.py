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

    assert updated_user._get_email() == new_email

def test__delete_user(database):
    email = "random.email@server.com"
    user = User(email=email)
    user.save()

    user = User.objects(email=email).first()

    user.delete()

    assert User.objects(email=email).first() == None

def test__fill_user_attr(database, load_user_data):
    print(f"load_user_data arg:{load_user_data}")
    user = User(**load_user_data)
    user.save()

    fields = { x:False for x in load_user_data.keys() }

    print(f"fields dict: {fields}")

    for k,v in user._data.items():
        if ( k in fields.keys() and load_user_data[k] == v ):
            # print(f"{k} found in fields: {fields[k]}")
            assert v == load_user_data[k]
            fields[k] = True
            # print(f"{k} field after: {fields[k]}")

    for k,v in fields.items():
        assert fields[k] == True
        

    # for k,v in user._data.items():
    #     try:
    #         print(f" caught loaded data: {load_user_data[k]}")
    #         # print(f"{k}: {v}")
    #     except Exception as error:
    #         print(f"error: {error}")
    # for k,v in load_user_data.items():
    #     print(f"{k}: {v}")
    
