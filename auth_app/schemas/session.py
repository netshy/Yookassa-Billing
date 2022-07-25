from marshm import ma
from models.db_models import Session


class SessionSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Session


SingleSessionSchema = SessionSchema()
MultipleSessionSchema = SessionSchema(many=True)
