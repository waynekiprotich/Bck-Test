from app.extensions import db
from app.models.group import Group, GroupMember
from app.utils.helpers import generate_invite_code


def create_group(admin_id: int, data: dict) -> Group:
    """
    Create a new group and automatically add the creator as a member.
    """
    group = Group(
        name=data.get("name", "").strip(),
        description=data.get("description", ""),
        invite_code=generate_invite_code(),
        admin_id=admin_id,
    )
    db.session.add(group)
    db.session.flush() 

    # Admin is automatically a member
    member = GroupMember(user_id=admin_id, group_id=group.id)
    db.session.add(member)
    db.session.commit()
    return group


def join_group(user_id: int, invite_code: str) -> Group:
    """
    Join an existing group by invite code.
    Raises ValueError if already a member.
    """
    group = Group.query.filter_by(invite_code=invite_code.upper()).first_or_404(
        description=f"No group found with invite code '{invite_code}'."
    )

    already_member = GroupMember.query.filter_by(
        user_id=user_id, group_id=group.id
    ).first()
    if already_member:
        raise ValueError("You are already a member of this group.")

    member = GroupMember(user_id=user_id, group_id=group.id)
    db.session.add(member)
    db.session.commit()
    return group


def get_user_groups(user_id: int):
    """Return all groups the user belongs to."""
    memberships = GroupMember.query.filter_by(user_id=user_id).all()
    group_ids = [m.group_id for m in memberships]
    return Group.query.filter(Group.id.in_(group_ids)).all()
