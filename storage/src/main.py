from flask import Flask, request, jsonify
from src.storage_service import StorageService
from config import Config
from src.utils.logger import LoggerManager

app = Flask(__name__)
config = Config()
logger = LoggerManager(__name__)
storage_service = StorageService()

@app.before_first_request
def initialize_database():
    logger.log_message("Initializing database...", level='info')
    storage_service.initialize_database()
    logger.log_message("Database initialized successfully", level='info')

@app.route('/documents/', methods=['POST'])
def create_document():
    try:
        data = request.json
        doc_id = storage_service.add_new_document(
            data['filename'],
            data['file_path'],
            data['file_size'],
            data['source_language'],
            data['target_language']
        )
        return jsonify({"id": doc_id}), 201
    except KeyError as e:
        logger.log_message(f"Missing required field: {str(e)}", level='error')
        return jsonify({"error": "Missing required field"}), 400
    except Exception as e:
        logger.log_message(f"Error creating document: {str(e)}", level='error')
        return jsonify({"error": "Internal server error"}), 500

@app.route('/documents/<int:doc_id>', methods=['GET'])
def get_document(doc_id):
    document = storage_service.get_document(doc_id)
    if document is None:
        return jsonify({"error": "Document not found"}), 404
    return jsonify(document)

@app.route('/documents/<int:doc_id>/status', methods=['PUT'])
def update_document_status(doc_id):
    new_status = request.json.get('status')
    if not new_status:
        return jsonify({"error": "Status is required"}), 400
    success = storage_service.update_document_status(doc_id, new_status)
    if not success:
        return jsonify({"error": "Document not found"}), 404
    return jsonify({"message": "Status updated successfully"})

@app.route('/documents/for_translation', methods=['GET'])
def get_documents_for_translation():
    limit = request.args.get('limit', default=10, type=int)
    offset = request.args.get('offset', default=0, type=int)
    documents = storage_service.get_documents_for_translation(limit, offset)
    return jsonify(documents)

@app.errorhandler(Exception)
def handle_exception(e):
    logger.log_message(f"Unhandled exception: {str(e)}", level='error')
    return jsonify({"error": "Internal server error"}), 500

if __name__ == "__main__":
    logger.log_message("Starting storage service...", level='info')
    app.run(host="0.0.0.0", port=8000, debug=config.DEBUG)
    logger.log_message("Storage service stopped", level='info')