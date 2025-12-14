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

@app.route('/flowers', methods=['GET', 'POST'])
@token_required
def manage_flowers():
    cur = mysql.connection.cursor()
    if request.method == 'GET':
        cur.execute("SELECT * FROM flower_list")
        rows = cur.fetchall()
        columns = [desc[0] for desc in cur.description]
        result = [dict(zip(columns, row)) for row in rows]
        return format_response(result)
    if request.method == 'POST':
        data = request.json
        required = ['name', 'color', 'season', 'seedling_cost', 'planting_month', 'watering_schedule', 'description']
        if not all(k in data for k in required):
            return jsonify({'message': 'Missing fields'}), 400
        sql = """INSERT INTO flower_list (name,color,season,seedling_cost,planting_month,watering_schedule,description)
                 VALUES (%s,%s,%s,%s,%s,%s,%s)"""
        cur.execute(sql, (data['name'], data['color'], data['season'], data['seedling_cost'], 
                          data['planting_month'], data['watering_schedule'], data['description']))
        mysql.connection.commit()
        return jsonify({'message': 'Flower created', 'id': cur.lastrowid}), 201

@app.route('/flowers/<int:id>', methods=['GET', 'PUT', 'DELETE'])
@token_required
def flower_detail(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM flower_list WHERE id=%s", (id,))
    row = cur.fetchone()
    if not row:
        return jsonify({'message': 'Flower not found'}), 404
    columns = [desc[0] for desc in cur.description]
    flower = dict(zip(columns, row))
    if request.method == 'GET':
        return format_response(flower)
    if request.method == 'PUT':
        data = request.json
        for field in ['name','color','season','seedling_cost','planting_month','watering_schedule','description']:
            if field not in data:
                data[field] = flower[field]
        sql = """UPDATE flower_list SET name=%s,color=%s,season=%s,seedling_cost=%s,planting_month=%s,
                 watering_schedule=%s,description=%s WHERE id=%s"""
        cur.execute(sql, (data['name'], data['color'], data['season'], data['seedling_cost'], 
                          data['planting_month'], data['watering_schedule'], data['description'], id))
        mysql.connection.commit()
        return jsonify({'message': 'Flower updated'})
    if request.method == 'DELETE':
        cur.execute("DELETE FROM flower_list WHERE id=%s", (id,))
        mysql.connection.commit()
        return jsonify({'message': 'Flower deleted'})

@app.route('/flowers/search', methods=['GET'])
def search_flowers():
    name = request.args.get('name')
    color = request.args.get('color')
    cur = mysql.connection.cursor()
    sql = "SELECT * FROM flower_list WHERE 1=1"
    params = []
    if name:
        sql += " AND name LIKE %s"
        params.append('%'+name+'%')
    if color:
        sql += " AND color LIKE %s"
        params.append('%'+color+'%')
    cur.execute(sql, tuple(params))
    rows = cur.fetchall()
    columns = [desc[0] for desc in cur.description]
    result = [dict(zip(columns,row)) for row in rows]
    return format_response(result)

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status":"OK"})

if __name__ == '__main__':
    app.run(debug=True)
