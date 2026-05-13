from flask import Blueprint, jsonify
from app.models.user import Institution
from app.schemas import institutions_schema

institutions_bp = Blueprint("institutions", __name__, url_prefix="/institutions")


@institutions_bp.get("/")
def get_institutions():
    # fetch all schools/bootcamps so the signup page can show them in the dropdown
    institutions = Institution.query.order_by(Institution.name).all()
    
    return institutions_schema.jsonify(institutions), 200