from flask import Flask
from flask import render_template, request
from flaskext import mysql
from datetime import datetime as dt

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

    sql = "Insert into rankingteams (name, country, manager, logo) values ('Paris Saint Germain', 'Francia', 'Mauricio Pochettino', 'https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.futbox.com%2Fes%2Fparis-saint-germain%23!informacion&psig=AOvVaw3qF4aDvH_82duJZP9SR0eg&ust=1638500074923000&source=images&cd=vfe&ved=0CAsQjRxqFwoTCIC7zsuOxPQCFQAAAAAdAAAAABAK');"
    
    cursor.execute(sql)

    conn.commit()

    return render_template('equipos/index.html')


@app.route('/create')
def create():
    return render_template('equipos/create.html')

@app.route('/store', methods=['POST'])
def storage():
    conn = mysql.connect()
    cursor = conn.cursor()

    sql = "Insert into rankingteams (name, country, manager, logo) values ('Bayern Munich', 'Alemania', 'Mauricio Pochettino', 'https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.futbox.com%2Fes%2Fparis-saint-germain%23!informacion&psig=AOvVaw3qF4aDvH_82duJZP9SR0eg&ust=1638500074923000&source=images&cd=vfe&ved=0CAsQjRxqFwoTCIC7zsuOxPQCFQAAAAAdAAAAABAK');"
    
    cursor.execute(sql)
    conn.commit()
    return render_template('equipos/index.html')

if __name__ == '__main__':
    app.run(debug=True)