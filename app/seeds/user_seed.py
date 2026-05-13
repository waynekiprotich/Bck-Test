from app.extensions import db
from app.models.user import User, Institution


def seed_users():
    moringa = Institution.query.filter_by(name="Moringa School").first()
    uon = Institution.query.filter_by(name="University of Nairobi").first()

    users_data = [
        dict(name="Alice Kamau",   email="alice@example.com",   password="password123", points=850,  institution=moringa),
        dict(name="Brian Otieno",  email="brian@example.com",   password="password123", points=620,  institution=moringa),
        dict(name="Carol Mwangi",  email="carol@example.com",   password="password123", points=430,  institution=uon),
        dict(name="David Njoroge", email="david@example.com",   password="password123", points=180,  institution=uon),
        dict(name="Eva Wanjiku",   email="eva@example.com",     password="password123", points=1200, institution=moringa),
        dict(name="Frank Kiprop",  email="frank@example.com",   password="password123", points=50,   institution=None),
    ]

    users = []
    for u in users_data:
        user = User(
            name=u["name"],
            email=u["email"],
            points=u["points"],
            institution=u["institution"],
        )
        user.set_password(u["password"])
        user.calculate_rank()
        db.session.add(user)
        users.append(user)

    db.session.commit()
    print(f"  ✓ {len(users)} users seeded")
    return users
