from flask import Flask
from flask import render_template, request, redirect
from flaskext import mysql
from datetime import datetime 
import os

app = Flask(__name__)
mysql = mysql.MySQL()

app.config['MYSQL_DATABASE_HOST'] = 'b6phvfwbvhi1c3mha7h9-mysql.services.clever-cloud.com'
app.config['MYSQL_DATABASE_USER'] = 'uo4gy1b7480dgnb4'
app.config['MYSQL_DATABASE_PASSWORD'] = 'UXmaMucXeSvvoQXxvcTJ'
app.config['MYSQL_DATABASE_DB'] = 'b6phvfwbvhi1c3mha7h9'

UPLOADS = os.path.join('src/uploads')
app.config['UPLOADS'] = UPLOADS # Guardo ruta como un valor en la app

mysql.init_app(app)

@app.route('/')
def index():
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

    _name = request.form['txtName']
    _country = request.form['txtCountry']
    _manager = request.form['txtManager']
    _logo = request.files['teamLogo']

    now = datetime.now()
    print(now)
    tiempo = now.strftime("%Y%H%M%S")
    print(tiempo)

    if _logo.filename != '':
        newNameLogo =  tiempo + '_' + _logo.filename
        _logo.save("uploads/" + newNameLogo)

    sql = "INSERT INTO rankingteams (name, country, manager, logo) values (%s, %s, %s, %s)"

    data = (_name, _country, _manager, _logo.filename)

    conn = mysql.connect()
    cursor = conn.cursor()

    cursor.execute(sql, data)
    conn.commit()
    return redirect('/')

@app.route('/delete/<int:id>')
def delete(id):
    sql = "DELETE FROM rankingteams WHERE id=%s"
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql, id)
    conn.commit()

    return redirect('/')

@app.route('/modify/<int:id>')
def modify(id):
    sql = "SELECT * FROM rankingteams WHERE id = %s"
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql, id)
    equipo = cursor.fetchone()
    conn.commit()

    return render_template('equipos/edit.html', equipo = equipo)

@app.route('/update', methods=['POST'])
def update():

    id = request.form['txtId']
    _name = request.form['txtName']
    _country = request.form['txtCountry']
    _manager = request.form['txtManager']
    _logo = request.files['teamLogo']

    data = (id, _name, _country, _manager)

    conn = mysql.connect()
    cursor = conn.cursor()

    if _logo.filename != '':
        now = datetime.now()
        tiempo = now.strftime("%Y%H%M%S")
        newNameLogo =  tiempo + '_' + _logo.filename
        _logo.save("uploads/" + newNameLogo)

    sql = "SELECT logo FROM rankingteams WHERE id=%s"
    cursor.execute(sql)

    nameLogo = cursor.fetchone()[0]

    os.remove(os.path.join(app.config['UPLOADS'], nameLogo))

    sql = "UPDATE rankingteams SET name = {_name}, country = {_country}, manager = {_manager} WHERE id = %s"

    cursor.execute(sql)
    conn.commit()

if __name__ == '__main__':
    app.run(debug=True)