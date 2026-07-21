from app.extensions import ma
from app.models import JobApplication
from marshmallow import EXCLUDE, fields, validate

class JobApplicationSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = JobApplication
        load_instance = True
        dump_only = ('id', 'date_updated')
        unknown = EXCLUDE


    status = fields.String(validate=validate.OneOf(['Applied', 'Interviewing', 'Offer', 'Rejected', 'Withdrawn']))
