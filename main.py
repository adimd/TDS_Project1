from flask import Flask, request, jsonify
import os
import task_manager

app = Flask(__name__)

# POST /run endpoint
@app.route('/run', methods=['POST'])
def run_task():
    """
    Executes a plain-English task.
    - If successful, returns HTTP 200 OK with the result.
    - If the task description is invalid, returns HTTP 400 Bad Request.
    - If there's an internal error, returns HTTP 500 Internal Server Error.
    """
   
    task_description = request.args.get('task')
    
    
    # Validate the task description
    if not task_description:
        return jsonify({"error": "Task description is required"}), 400
    
    try:
        # Execute the task
        result = task_manager.execute_task(task_description)
        return jsonify(result), 200
    except ValueError as e:
        # Handle errors in the task description
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        # Handle internal errors
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500

# GET /read endpoint
@app.route('/read', methods=['GET'])
def read_file():

    file_path = request.args.get('path')
    
    # Validate the file path
    if not file_path:
        return jsonify({"error": "File path is required"}), 400
    
    # Check if the file exists
    if not os.path.exists(file_path):
        return "", 404
    
    try:
        # Read and return the file content
        with open(file_path, 'r') as file:
            content = file.read()
        return content, 200
    except Exception as e:
        # Handle internal errors
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)