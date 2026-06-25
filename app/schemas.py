from app.extensions import ma
from app.models import JobApplication
from marshmallow import EXCLUDE

class JobApplicationSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = JobApplication
        load_instance = True
        dump_only = ('id', 'date_updated')
        unknown = EXCLUDE
