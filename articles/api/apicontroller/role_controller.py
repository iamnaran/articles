from articles import db
from articles.models.Role import Role
from articles.models.Role import role_schema


def get_all_roles():
    all_roles = Role.query.all()
    return role_schema.dump(all_roles)


def create_new_role(roleName):
    role = Role(role_name=roleName)
    db.session.add(role)
    db.session.commit()
    return role_schema.dump(role)


