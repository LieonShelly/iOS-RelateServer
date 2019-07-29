from App.Log import log_api
from flask import send_from_directory, current_app

@log_api.route('/get', methods=['GET'])
def get_log():
    file_response = send_from_directory(directory=current_app.config['BASE_DIR'], filename="output.log", as_attachment=True)
    return file_response
