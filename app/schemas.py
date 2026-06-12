from app.extensions import ma
from app.models import JobApplication

class JobApplicationSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = JobApplication
        load_instance = True
