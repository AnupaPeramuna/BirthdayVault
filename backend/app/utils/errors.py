import logging
from flask import Blueprint, jsonify

error_bp = Blueprint('errors', __name__, url_prefix='/errors')

@error_bp.app_errorhandler(404)
def not_found(error):
    logging.error(error)
    return jsonify({"error": "Not Found"}), 404

@error_bp.app_errorhandler(Exception)
def unhandled_exception(error):
    logging.error(error)
    return jsonify({"error": "Unhandled Exception"}), 500

