from app.extensions import db
from app.models.user import Institution


def seed_institutions():
    institutions = [
        Institution(name="Moringa School", type="Bootcamp"),
        Institution(name="ALX Africa", type="Bootcamp"),
        Institution(name="Andela", type="Bootcamp"),
        Institution(name="University of Nairobi", type="University"),
        Institution(name="Strathmore University", type="University"),
        Institution(name="JKUAT", type="University"),
        Institution(name="Kenyatta University", type="University"),
        Institution(name="Other", type="University"),
    ]
    db.session.add_all(institutions)
    db.session.commit()
    print(f"  ✓ {len(institutions)} institutions seeded")
    return institutions
