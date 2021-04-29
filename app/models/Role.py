from app import db, login_manager, ma
from marshmallow import fields, validate


class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String(100), unique=True)

    def __repr__(self):
        return f"Role('{self.id}','{self.role_name}')"


class RoleSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        # Fields to expose
        model = Role

    id = fields.Integer(dump_only=True)
    role_name = fields.String(required=True, validate=validate.Length(min=3, max=40))


role_schema = RoleSchema()
roles_schema = RoleSchema(many=True)
