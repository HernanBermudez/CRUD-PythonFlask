from flask import Flask
from flask import render_template, request, redirect
from flaskext import mysql
from datetime import datetime 

app = Flask(__name__)
mysql = mysql.MySQL()

app.config['MYSQL_DATABASE_HOST'] = 'b6phvfwbvhi1c3mha7h9-mysql.services.clever-cloud.com'
app.config['MYSQL_DATABASE_USER'] = 'uo4gy1b7480dgnb4'
app.config['MYSQL_DATABASE_PASSWORD'] = 'UXmaMucXeSvvoQXxvcTJ'
app.config['MYSQL_DATABASE_DB'] = 'b6phvfwbvhi1c3mha7h9'

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
    
if __name__ == '__main__':
    app.run(debug=True)