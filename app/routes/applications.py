from flask import Blueprint, jsonify, request
from app.models import JobApplication
from app.extensions import db
from app.schemas import JobApplicationSchema
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import date


applications_bp = Blueprint('applications', __name__)
application_schema = JobApplicationSchema()
applications_schema = JobApplicationSchema(many=True)

# GET all applications
@applications_bp.route('/applications', methods=['GET'])
@jwt_required()
def get_applications():
    applications = db.session.execute(db.select(JobApplication).where(JobApplication.user_id == int(get_jwt_identity()))).scalars().all()

    return jsonify(applications_schema.dump(applications)), 200

# CREATE a new application
@applications_bp.route('/applications', methods=['POST'])
@jwt_required()
def create_application():
    data = request.get_json()
    new_application = application_schema.load(data)
    new_application.date_updated = date.today().isoformat()
    new_application.user_id = int(get_jwt_identity())
    db.session.add(new_application)
    db.session.commit()
    return jsonify(application_schema.dump(new_application)), 201


# GET a specific application by ID
@applications_bp.route('/applications/<int:id>', methods=['GET'])
@jwt_required()
def get_application(id):
    application = db.get_or_404(JobApplication, id)
    if application.user_id != int(get_jwt_identity()):
        return jsonify({'message': 'Unauthorized'}), 403
    
    return jsonify(application_schema.dump(application))


# UPDATE an existing applicaition by ID
@applications_bp.route('/applications/<int:id>', methods=['PUT'])
@jwt_required()
def update_application(id):
    application = db.get_or_404(JobApplication, id)
    if application.user_id != int(get_jwt_identity()):
        return jsonify({'message': 'Unauthorized'}), 403
    

    data = request.get_json()

    application = application_schema.load(data, instance=application, partial=True)
    db.session.commit()
    return jsonify(application_schema.dump(application))


# DELETE an application by ID
@applications_bp.route('/applications/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_application(id):
    application = db.get_or_404(JobApplication, id)

    if application.user_id != int(get_jwt_identity()):
        return jsonify({'message': 'Unauthorized'}), 403

    db.session.delete(application)
    db.session.commit()
    return ('', 204)