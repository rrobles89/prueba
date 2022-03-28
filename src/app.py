from flask import Flask,jsonify,request,render_template
from users import users
import csv
import mysql.connector
from mysql.connector import Error



app = Flask(__name__)

#Insersión de clientes
@app.route('/',methods=['GET'])
def save_file():
    global connection
    try:
        if total_clientes() != 0 :
            return jsonify({"response":"El archivo ya fue cargado"})
        
        connection = mysql.connector.connect(
        host='127.0.0.1',
        port=3306,
        user='root',
        password='root',
        db='db_customers'
    )

        if connection.is_connected():
            print("Conexión exitosa.")
            infoServer = connection.get_server_info()
            print("Info del servidor: {}".format(infoServer))
            cursor = connection.cursor()  
            with connection.cursor() as cursor:
                #with open('clientes/clientes.csv', 'r') as csvFile: #Ruta en Docker 
                with open('/app/src/clientes/clientes.csv', 'r') as csvFile:
                    next(csvFile)
                    reader = csv.reader(csvFile, delimiter=',')
                    for row in reader:
                            consulta = "INSERT INTO client(id_client,first_name,last_name,email,gender,company,city,title,lat,longi) VALUES (%s,%s,%s,%s,%s,%s, %s,%s,%s,%s);"
                            
                            cursor.execute(consulta, (int(row[0]),str(row[1]),str(row[2]),str(row[3]),str(row[4]),str(row[5]),str(row[6]),str(row[7]),'1','1'))     
                    csvFile.close()           
                    connection.commit()
    except Error as ex:
        print("Error durante la conexión: {}".format(ex))
    finally:
        if connection.is_connected():
            connection.close() 
            print("La conexión ha finalizado.")
    return jsonify({"response":"Archivo Cargado"})


#Listado de clientes
@app.route('/listado',methods=['GET'])
def usuarios():
    global connection
    try:
        connection = mysql.connector.connect(
            host='127.0.0.1',
            port=3306,
            user='root',
            password='root',
            db='db_customers'
        )
        if connection.is_connected():
            print("Conexión exitosa.")
            infoServer = connection.get_server_info()
            print("Info del servidor: {}".format(infoServer))
            cursor = connection.cursor() 
            cursor.execute("SELECT * FROM client;") 
            myresult = cursor.fetchall() 
    except Error as ex:
        print("Error durante la conexión: {}".format(ex))
    finally:
        if connection.is_connected():
            connection.close()
            print("La conexión ha finalizado.")
    
    return render_template("index.html",lista =myresult)


#Busqueda de cliente por su id
@app.route('/usuario/<int:id>',methods=['GET'])
def usuario(id):
    global connection
    try:
        connection = mysql.connector.connect(
            host='127.0.0.1',
            port=3306,
            user='root',
            password='root',
            db='db_customers'
        )
        if connection.is_connected():
            print("Conexión exitosa.")
            infoServer = connection.get_server_info()
            print("Info del servidor: {}".format(infoServer))
            cursor = connection.cursor() 
            cursor.execute("SELECT * FROM client where id_client="+str(id)+";") 
            myresult = cursor.fetchall() 
    except Error as ex:
        print("Error durante la conexión: {}".format(ex))
    finally:
        if connection.is_connected():
            connection.close()
            print("La conexión ha finalizado.")
    
    return jsonify({"response":myresult})


#Actualiza latitud y longitud mediante el id de cliente
@app.route('/actualizar',methods=['POST'])
def actualizar():
    json = request.get_json()
    global connection
    try:
        connection = mysql.connector.connect(
            host='127.0.0.1',
            port=3306,
            user='root',
            password='root',
            db='db_customers'
        )
        if connection.is_connected():
            print("Conexión exitosa.")
            infoServer = connection.get_server_info()
            print("Info del servidor: {}".format(infoServer))
            cursor = connection.cursor() 
            cursor.execute("UPDATE client set lat="+ json.get('latitud') + ",longi= "+ json.get('longitud')+ " where id_client="+str(json.get('id'))+";") 
            connection.commit()
    except Error as ex:
        print("Error durante la conexión: {}".format(ex))
    finally:
        if connection.is_connected():
            connection.close() 
            print("La conexión ha finalizado.")
    
    return jsonify({"response":"Se Actualizo Correctamente"})


#Tota de clientes
@app.route('/total',methods=['GET'])
def total_clientes():
    global connection
    global total
    try:
        connection = mysql.connector.connect(
            host='127.0.0.1',
            port=3306,
            user='root',
            password='root',
            db='db_customers'
        )
        if connection.is_connected():
            print("Conexión exitosa.")
            infoServer = connection.get_server_info()
            print("Info del servidor: {}".format(infoServer))
            cursor = connection.cursor() 
            cursor.execute("SELECT count(*) total FROM client;") 
            myresult = cursor.fetchall() 
            for element in myresult:
                total = int(element[0])
    except Error as ex:
        print("Error durante la conexión: {}".format(ex))
    finally:
        if connection.is_connected():
            connection.close()
            print("La conexión ha finalizado.")
        
    return int(total)



@app.route("/users")
def usersHandler():
    return jsonify({"users": users})

if __name__ == '__main__':
    app.run(host="0.0.0.0",port=4000,debug=True)

