
from flask import request, Response, jsonify
from file_storage import save_binary_file
from crypto_hash import hash_file

def setup_routes(app):
    @app.route('/ping', methods=['GET', 'POST'])
    def ping():
        return jsonify({
            "Ready": "Service ready"
        })

    @app.route('/upload', methods=['PUT'])
    def upload():
        file_data = request.data
        if not file_data:
            return jsonify({"error": "No data provided"}), 400

        try:
            file_guid = save_binary_file(file_data)
        except Exception as e:
            return jsonify({"error": str(e)}), 500

        resp = Response(status=201)
        resp.headers['X-New-Name'] = file_guid
        return resp

    @app.route('/api/v3.1/crypto/hash', methods=['POST'])
    def crypto_hash_route():
        # Проверяем Content-Type
        if not request.is_json:
            return jsonify({"status": "fail", "data": "Content-Type must be application/json"}), 400

        params = request.get_json()
        status, data = hash_file(params)

        if status == "success":
            return jsonify({"status": "success", "data": data}), 200
        else:
            return jsonify({"status": "fail", "data": data}), 400
