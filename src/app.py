from flask import Flask
from flask import render_template
from flaskext import mysql

app = Flask(__name__)
mysql = mysql.MySQL()

app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'rootroot'
app.config['MYSQL_DATABASE_DB'] = 'equipos_db'

mysql.init_app(app)

@app.route('/')
def index():
    conn = mysql.connect()
    cursor = conn.cursor()

    sql = "Insert into equipos (nombre, pais, tecnico, escudo) values ('Paris Saint Germain', 'Francia', 'Mauricio Pochettino', 'https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.futbox.com%2Fes%2Fparis-saint-germain%23!informacion&psig=AOvVaw3qF4aDvH_82duJZP9SR0eg&ust=1638500074923000&source=images&cd=vfe&ved=0CAsQjRxqFwoTCIC7zsuOxPQCFQAAAAAdAAAAABAK');"
    
    cursor.execute(sql)

    conn.commit()

    return render_template('equipos/index.html')

if __name__ == '__main__':
    app.run(debug=True)