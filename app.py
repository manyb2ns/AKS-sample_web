from flask import Flask, render_template, jsonify

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

# 테스트용 Mock API
@app.route("/api/mock-data", methods=["GET"])
def mock_data():
    mock_response = {
        "status": "success",
        "data": {
            "id": 123123,
            "name": "Mock Item",
            "description": "This is a mock item for testing."
        }
    }
    return jsonify(mock_response)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)