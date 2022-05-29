import os
from datetime import datetime
from flask import Flask
from flask import render_template, request, redirect, send_from_directory
from flaskext import mysql

app = Flask(__name__)
mysql = mysql.MySQL()

app.config['MYSQL_DATABASE_HOST'] = 'b6phvfwbvhi1c3mha7h9-mysql.services.clever-cloud.com'
app.config['MYSQL_DATABASE_USER'] = 'uo4gy1b7480dgnb4'
app.config['MYSQL_DATABASE_PASSWORD'] = 'UXmaMucXeSvvoQXxvcTJ'
app.config['MYSQL_DATABASE_DB'] = 'b6phvfwbvhi1c3mha7h9'

UPLOADS = os.path.join('src/uploads')
app.config['UPLOADS'] = UPLOADS # Guardo ruta como un valor en la app

mysql.init_app(app)
conn = mysql.connect()
cursor = conn.cursor()

def query_mysql(query, data):
    """Function for mysql queries"""
    if len(data) > 0:
        cursor.execute(query, data)
    else:
        cursor.execute(query)
    conn.commit()

@app.route('/')
def index():
    """Index template. Will show teams in database"""
    conn = mysql.connect()
    cursor = conn.cursor()
    sql = "SELECT * FROM rankingteams;"
    cursor.execute(sql)
    equipos = cursor.fetchall()
    print(equipos)
    conn.commit()
    return render_template('equipos/index.html', equipos = equipos)

@app.route('/create')
def create():
    return render_template('equipos/create.html')

@app.route('/store', methods=['POST'])
def storage():
    """Stores new team in database"""
    _name = request.form['txtName']
    _country = request.form['txtCountry']
    _manager = request.form['txtManager']
    _logo = request.form['teamLogo']

    now = datetime.now()
    print(now)
    tiempo = now.strftime("%Y%H%M%S")
    print(tiempo)

    sql = "INSERT INTO rankingteams (name, country, manager, logo_url) values (%s, %s, %s, %s)"
    data = (_name, _country, _manager, _logo)
    query_mysql(sql, data)
    return redirect('/create')

@app.route('/delete/<int:id>')
def delete(id):
    """Deletes team from database"""
    sql = f'DELETE FROM rankingteams WHERE id="{id}"'
    cursor.execute(sql)
    conn.commit()
    return redirect('/')

@app.route('/modify/<int:id>')
def modify(id):
    """Modifies teams in database"""
    sql = "SELECT * FROM rankingteams WHERE id = %s"
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql, id)
    equipo = cursor.fetchone()
    conn.commit()
    return render_template('equipos/edit.html', equipo = equipo)

@app.route('/update', methods=['POST'])
def update():
    """Updates team from database"""
    _id = request.form['txtId']
    _name = request.form['txtName']
    _country = request.form['txtCountry']
    _manager = request.form['txtManager']
    _logo = request.form['teamLogo']

    conn = mysql.connect()
    cursor = conn.cursor()

    sql = f'UPDATE rankingteams SET name = "{_name}", country = "{_country}", manager = "{_manager}", logo_url = "{_logo}" WHERE id = "{_id}"'
    cursor.execute(sql)
    conn.commit()
    return redirect('/')

@app.route('/reset-ids')
def reset():
    """Resets auto increment of IDs from database"""
    data = []
    sql = f"ALTER TABLE b6phvfwbvhi1c3mha7h9.rankingteams auto_increment = 0;"
    query_mysql(sql, data)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)