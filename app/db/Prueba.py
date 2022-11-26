import psycopg2

connection = psycopg2.connect(
    host="localhost",
    user="postgres",
    password="root",
    dbname="postgres",
    port="5432"
)

connection.autocommit = True


def crearTabla():
    cursor = connection.cursor()
    query = "CREATE TABLE usuario(id varchar(30),nombre varchar(30),apellido varchar(30), direccion varchar(30), telefono numeric(10))"
    try:
        cursor.execute(query)
    except:
        print("La tabla Usuarios ya existe")
    cursor.close()


def insertarDatos():
    cursor = connection.cursor()
    query = f""" INSERT INTO usuario (id,nombre,apellido,direccion,telefono) values ('12','andres','brieva','calle 5#14-42', 3004992478)"""
    cursor.execute(query)
    cursor.close()


def eliminarTabla():
    cursor = connection.cursor()
    query = "DROP TABLE usuario"
    cursor.execute(query)
    cursor.close()


def actualizarDatos():
    cursor = connection.cursor()
    query = """ UPDATE usuario set nombre = 'camilo' where id = '13' """
    try:
        cursor.execute(query)
    except:
        print("No se encuentra el usuario")
    cursor.close()


# crearTabla()
# insertarDatos()
eliminarTabla()
# actualizarDatos()
