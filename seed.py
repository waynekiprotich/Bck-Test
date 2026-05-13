from app import create_app
from app.extensions import db
from app.seeds.run_all import run_all

app = create_app("development")

with app.app_context():
    print("Dropping all tables...")
    db.drop_all()
    print("Creating all tables...")
    db.create_all()
    print("Seeding data...")
    run_all()
    print("\nDatabase seeded successfully!")
