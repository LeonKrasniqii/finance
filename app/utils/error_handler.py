from flask import jsonify

def handle_error(message, code=400):
    return jsonify({"error": message}), code
