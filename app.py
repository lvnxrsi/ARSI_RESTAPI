print(">>> RUNNING CORRECT app.py <<<")
from flask import Flask, request, jsonify, make_response
from flask_mysqldb import MySQL
import jwt
import datetime
from functools import wraps
from dicttoxml import dicttoxml
from db import MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB, MYSQL_PORT, JWT_SECRET, JWT_ALGORITHM, JWT_EXPIRE_SECONDS

app = Flask(__name__)

app.config['MYSQL_HOST'] = MYSQL_HOST
app.config['MYSQL_USER'] = MYSQL_USER
app.config['MYSQL_PASSWORD'] = MYSQL_PASSWORD
app.config['MYSQL_DB'] = MYSQL_DB
app.config['MYSQL_PORT'] = MYSQL_PORT

mysql = MySQL(app)

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('x-access-token')
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        try:
            jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        except Exception:
            return jsonify({'message': 'Token is invalid!'}), 401
        return f(*args, **kwargs)
    return decorated

@app.route('/login', methods=['POST'])
def login():
    auth = request.json
    if not auth or not auth.get('username') or not auth.get('password'):
        return make_response('Missing credentials', 400)
    if auth['username'] == 'admin' and auth['password'] == 'admin':
        token = jwt.encode({
            'user': auth['username'],
            'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=JWT_EXPIRE_SECONDS)
        }, JWT_SECRET, algorithm=JWT_ALGORITHM)
        return jsonify({'token': token})
    return make_response('Invalid credentials', 401)

def format_response(data):
    fmt = request.args.get('format', 'json').lower()
    if fmt == 'xml':
        return app.response_class(dicttoxml(data), mimetype='application/xml')
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
