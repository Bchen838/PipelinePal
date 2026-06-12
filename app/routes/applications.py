from flask import Blueprint, jsonify, request
from app.models import JobApplication
from app.extensions import db
from app.schemas import JobApplicationSchema
from flask_jwt_extended import jwt_required

applications_bp = Blueprint('applications', __name__)
application_schema = JobApplicationSchema()
applications_schema = JobApplicationSchema(many=True)


@applications_bp.route('/applications', methods=['GET'])
@jwt_required()
def get_applications():
    applications = db.session.execute(db.select((JobApplication))).scalars().all()

    return jsonify(applications_schema.dump(applications))


@applications_bp.route('/applications', methods=['POST'])
@jwt_required()
def create_application():
    data = request.get_json()
    new_application = application_schema.load(data)

    db.session.add(new_application)
    db.session.commit()
    return jsonify(application_schema.dump(new_application)), 201


@applications_bp.route('/applications/<int:id>', methods=['GET'])
@jwt_required()
def get_application(id):
    application = db.get_or_404(JobApplication, id)
    return jsonify(application_schema.dump(application))


@applications_bp.route('/applications/<int:id>', methods=['PUT'])
@jwt_required()
def update_application(id):
    application = db.get_or_404(JobApplication, id)
    data = request.get_json()

    application = application_schema.load(data, instance=application, partial=True)
    db.session.commit()
    return jsonify(application_schema.dump(application))


@applications_bp.route('/applications/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_application(id):
    application = db.get_or_404(JobApplication, id)
    db.session.delete(application)
    db.session.commit()
    return ('', 204)