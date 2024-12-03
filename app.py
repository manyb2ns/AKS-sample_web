from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/page1')
def page1():
    return render_template('page1.html')

@app.route('/page2')
def page2():
    return render_template('page2.html')

################################## 테스트용 Mock API ##################################
# in-memory db (for mock)
mock_data = {
    1: {"id": 1, "name": "Item 1", "description": "This is the first mock item."},
    2: {"id": 2, "name": "Item 2", "description": "This is the second mock item."},
}

# GET: Fetch all items
@app.route("/api/items", methods=["GET"])
def get_items():
    return jsonify({"status": "success", "data": list(mock_data.values())})

# GET: Fetch a specific item by ID
@app.route("/api/items/<int:item_id>", methods=["GET"])
def get_item(item_id):
    item = mock_data.get(item_id)
    if item:
        return jsonify({"status": "success", "data": item})
    else:
        return jsonify({"status": "error", "message": "Item not found"}), 404
    
# POST: Add a new item
@app.route("/api/items", methods=["POST"])
def add_item():
    data = request.json
    if not data or "name" not in data or "description" not in data:
        return jsonify({"status": "error", "message": "Invalid data"}), 400

    new_id = max(mock_data.keys(), default=0) + 1
    new_item = {"id": new_id, "name": data["name"], "description": data["description"]}
    mock_data[new_id] = new_item
    return jsonify({"status": "success", "data": new_item}), 201

# PUT: Update an existing item
@app.route("/api/items/<int:item_id>", methods=["PUT"])
def update_item(item_id):
    data = request.json
    if item_id not in mock_data:
        return jsonify({"status": "error", "message": "Item not found"}), 404

    if not data or "name" not in data or "description" not in data:
        return jsonify({"status": "error", "message": "Invalid data"}), 400

    updated_item = {"id": item_id, "name": data["name"], "description": data["description"]}
    mock_data[item_id] = updated_item
    return jsonify({"status": "success", "data": updated_item})

# DELETE: Delete an item by ID
@app.route("/api/items/<int:item_id>", methods=["DELETE"])
def delete_item(item_id):
    if item_id in mock_data:
        deleted_item = mock_data.pop(item_id)
        return jsonify({"status": "success", "data": deleted_item})
    else:
        return jsonify({"status": "error", "message": "Item not found"}), 404

######################################################################################

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)