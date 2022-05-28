from flask import Flask
from flask import render_template, request, redirect, url_for, send_from_directory
from flaskext import mysql
from datetime import datetime 
import os

from pymysql import STRING

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

def queryMySQL(query, data):
    if len(data) > 0:
        cursor.execute(query, data)
    else:
        cursor.execute(query)
    conn.commit()

@app.route('/logoteam/<path:nameLogo>')
def showLogo(nameLogo):
    return send_from_directory(os.path.join('uploads'), nameLogo)

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
        # _logo.save("src/uploads/" + newNameLogo)

    sql = "INSERT INTO rankingteams (name, country, manager, logo) values (%s, %s, %s, %s)"

    data = (_name, _country, _manager, newNameLogo)

    queryMySQL(sql, data) # lo mismo pero con función
    # conn = mysql.connect()
    # cursor = conn.cursor()

    # cursor.execute(sql, data)
    # conn.commit()
    return redirect('/create')

@app.route('/delete/<int:id>')
def delete(id):
    conn = mysql.connect()
    cursor = conn.cursor()
    sql = f'SELECT logo FROM rankingteams logo WHERE id="{id}"'
    cursor.execute(sql)
    conn.commit()
    nameLogo = cursor.fetchone()[0]
    try:
        sql = f'DELETE logo FROM rankingteams logo WHERE id="{id}"'
        cursor.execute(sql)
        conn.commit()
        # os.remove(os.path.join(app.config['UPLOADS'], nameLogo))
    except:
        print("No borró el logo")

    sql = f'DELETE FROM rankingteams WHERE id="{id}"'
 
    cursor.execute(sql)
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

    # data = (id, _name, _country, _manager)

    conn = mysql.connect()
    cursor = conn.cursor()

    if _logo.filename != '':
        now = datetime.now()
        tiempo = now.strftime("%Y%H%M%S")
        newNameLogo =  tiempo + '_' + _logo.filename
        # _logo.save("src/uploads/" + newNameLogo)

        sql = f'SELECT logo FROM rankingteams logo WHERE id="{id}"'
        cursor.execute(sql)
        conn.commit()

        nameLogo = cursor.fetchone()[0]
        os.path.join(app.config['UPLOADS'], nameLogo)  

        try:
            os.remove(os.path.join(app.config['UPLOADS'], nameLogo))
            sql = f'UPDATE rankingteams SET logo = "{newNameLogo}" WHERE id="{id}";'
            cursor.execute(sql)
            conn.commit()
        except:
            print("No borró el logo anterior")

    sql = f'UPDATE rankingteams SET name = "{_name}", country = "{_country}", manager = "{_manager}" WHERE id = "{id}"'
    cursor.execute(sql)
    conn.commit()

    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)