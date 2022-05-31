from flask import Flask, render_template,request,redirect,url_for,flash,json,jsonify
from flask_mysqldb import MySQL,MySQLdb

app = Flask(__name__)
#conexion con mysql
app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']='1234'
app.config['MYSQL_DB']='Proyecto'
mysql = MySQL(app)

#configuracion de datos de la app
app.secret_key = 'mysecretkey'

@app.route('/')#al poner solo el / indico que la primer pagina que se retornara al iniciar la aplicacion sera home.html
def home():
    return render_template('home.html')

@app.route('/leds',strict_slashes=False)
def leds():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM Leds")
    data = cur.fetchall()
    #print(data)
    return render_template('leds.html',valores = data)
    
@app.route('/datos_leds',methods=['POST'])#uso esta ruta para recibir los datos de los leds
def add_datos_leds():
    if request.method == 'POST':
        ledred = request.form['rinput']
        ledgreen = request.form['ginput']
        ledblue = request.form['binput']
        print(ledred)#borrar esto
        print(ledgreen)#borrar esto
        print(ledblue)#borrar esto
        
        cur = mysql.connection.cursor()#aqui obtengo la conexion a la base de datos
        cur.execute('INSERT INTO Leds (vred,vgreen,vblue,fecha) VALUES (%s,%s,%s,current_timestamp())',(ledred,ledgreen,ledblue))#consulta que se ejecutara
        mysql.connection.commit()

        flash('Dato agregado de manera correcta')

        return redirect(url_for('leds'))

@app.route('/datos_json')#ruta de prueba para json
def convert_json():
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT * FROM Leds")
    rv = cur.fetchall()
    leds = []
    content = {}
    for result in rv:
        content = {'vred':result['vred'],'vgreen':result['vgreen'],'vblue':result['vblue']}
        leds.append(content)
        content = {}
    return jsonify(leds) 
    
@app.route('/pruebas', strict_slashes=False)
def pruebas():
    return render_template('pruebas.html')

#ruta para borrar batos
@app.route('/delete/<string:id>')
def delete_val(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM Leds WHERE id = {0}".format(id))
    mysql.connection.commit()
    flash('Dato eliminado de manera correcta')
    return redirect(url_for('leds'))
if __name__ == '__main__':
    app.run(debug=True)

