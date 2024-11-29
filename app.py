from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    #return "<h1>Welcome to the Home Page</h1><p>This is the main page of our application.</p>"
    return render_template('home.html')

@app.route('/page1')
def page1():
    #return "<h1>Page 1</h1><p>This is the content for Page 1.</p>"
    return render_template('page1.html')

@app.route('/page2')
def page2():
    #return "<h1>Page 2</h1><p>This is the content for Page 2.</p>"
    return render_template('page2.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
    # app.run(debug=True)