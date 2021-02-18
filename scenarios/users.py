from application.app import create_app
from application.models import db, User


app = create_app("development")


def run():
    with app.app_context():
        
        print(f"ran users script. DB: {db}")

        db.drop_all()
        db.create_all()

        # Admin user
        admin = User(email="admin@server.com")
        db.session.add(admin)

        # First base user
        user1 = User(email="user1@server.com")
        db.session.add(user1)

        # Second base user
        user2 = User(email="user2@server.com")
        db.session.add(user2)

        print(f"user.first(): {User.query.first()}")

        db.session.commit()