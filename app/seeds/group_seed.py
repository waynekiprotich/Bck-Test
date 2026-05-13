from app.extensions import db
from app.models.user import User
from app.models.group import Group, GroupMember
from app.utils.helpers import generate_invite_code


def seed_groups():
    alice = User.query.filter_by(email="alice@example.com").first()
    brian = User.query.filter_by(email="brian@example.com").first()
    carol = User.query.filter_by(email="carol@example.com").first()
    eva   = User.query.filter_by(email="eva@example.com").first()

    groups_data = [
        {
            "name": "Moringa Coders",
            "description": "Official Moringa School coding group",
            "admin": alice,
            "members": [alice, brian, eva],
        },
        {
            "name": "UoN Dev Club",
            "description": "University of Nairobi developers",
            "admin": carol,
            "members": [carol],
        },
    ]

    created = []
    for g in groups_data:
        group = Group(
            name=g["name"],
            description=g["description"],
            invite_code=generate_invite_code(),
            admin_id=g["admin"].id,
        )
        db.session.add(group)
        db.session.flush()

        for user in g["members"]:
            member = GroupMember(user_id=user.id, group_id=group.id)
            db.session.add(member)

        created.append(group)

    db.session.commit()
    print(f"  ✓ {len(created)} groups seeded")
    return created
