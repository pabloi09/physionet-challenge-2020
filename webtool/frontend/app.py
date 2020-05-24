from flask import Flask

app = Flask(__name__, static_folder='./build', static_url_path='/')

@app.route('/')
def index():
    return app.send_static_file('index.html')

if __name__ == '__main__':
   app.run(port=3000, debug=True, host='0.0.0.0')