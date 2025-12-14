print(">>> RUNNING CORRECT app.py <<<")
from flask import Flask
from flask_mysqldb import MySQL
from db import MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB, MYSQL_PORT

app = Flask(__name__)

app.config['MYSQL_HOST'] = MYSQL_HOST
app.config['MYSQL_USER'] = MYSQL_USER
app.config['MYSQL_PASSWORD'] = MYSQL_PASSWORD
app.config['MYSQL_DB'] = MYSQL_DB
app.config['MYSQL_PORT'] = MYSQL_PORT

mysql = MySQL(app)

if __name__ == '__main__':
    app.run(debug=True)
