from app.seeds.institution_seed import seed_institutions
from app.seeds.user_seed import seed_users
from app.seeds.challenge_seed import seed_challenges
from app.seeds.group_seed import seed_groups


def run_all():
    """
    Run all seed functions in dependency order.
    Institutions must exist before users.
    Users must exist before groups.
    Challenges must exist before weekly challenges (seeded inside challenge_seed).
    """
    print("\nSeeding institutions...")
    seed_institutions()

    print("Seeding users...")
    seed_users()

    print("Seeding challenges + test cases + weekly challenge...")
    seed_challenges()

    print("Seeding groups...")
    seed_groups()

    print("\nAll seeds complete.")
