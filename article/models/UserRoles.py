from article import db, ma
from marshmallow import fields, validate


class UserRoles(db.Model):
    __tablename__ = 'user_roles'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    role_id = db.Column(db.Integer(), db.ForeignKey('roles.id', ondelete='CASCADE'), nullable=False)


class UserRoleSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        # Fields to expose
        model = UserRoles

    id = fields.Integer(dump_only=True)
    user_id = fields.String(required=True)
    role_id = fields.String(required=True)


role_schema = UserRoleSchema()
roles_schema = UserRoleSchema(many=True)
