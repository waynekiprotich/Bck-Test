from app.extensions import db
from app.models.group import Group, GroupMember
from app.utils.helpers import generate_invite_code


def create_group(admin_id: int, data: dict) -> Group:
    group = Group(
        name=data.get("name", "").strip(),
        description=data.get("description", ""),
        invite_code=generate_invite_code(),
        admin_id=admin_id,
    )
    db.session.add(group)
    
    # flush to get the new group.id before committing the whole transaction!
    db.session.flush() 

    # make sure the person who created the group is actually in it
    member = GroupMember(user_id=admin_id, group_id=group.id)
    db.session.add(member)
    db.session.commit()
    
    return group


def join_group(user_id: int, invite_code: str) -> Group:
    # force uppercase just in case the user typed it with lowercase letters
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
    # find all junction table memberships first, then grab the actual group details
    memberships = GroupMember.query.filter_by(user_id=user_id).all()
    group_ids = [m.group_id for m in memberships]
    
    return Group.query.filter(Group.id.in_(group_ids)).all()