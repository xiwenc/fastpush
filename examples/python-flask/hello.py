from flask import Flask
import os

app = Flask(__name__)

port = int(os.getenv("PORT", 9099))


@app.route('/')
def hello_world():
    return """
<!DOCTYPE html>
<html>
    <head>
        <link rel="stylesheet" type="text/css" href="sample.css">
    </head>
    <body>
        <h1>Hello there World</h1>
    </body>
</html>
"""


@app.route('/sample.css')
def static_proxy():
    with open('sample.css') as f:
        return f.read(), 200, {'Content-Type': 'text/css; charset=utf-8'}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port)
