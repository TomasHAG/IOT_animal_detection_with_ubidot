import mysql.connector

config = {
  'user': 'root',
  'password': 'myRootPassword123',
  'host': 'localhost',
  'database': 'Db',
  'raise_on_warnings': True
}

def get_config():
    return config

def connect():
    cnx = mysql.connector.connect(**config)
    return cnx, cnx.cursor()

def create_table():
    cnx, cursor = connect()
    cursor.execute("CREATE TABLE detection (device_id CHAR(50), time DATETIME(6) KEY UNIQUE, temperature DOUBLE, humidity INT, wind DOUBLE, clouds INT, sensor_trigger INT)")
    cnx.commit()

    #create user for grafana
    cursor.execute("CREATE USER 'grafanaReader' IDENTIFIED BY 'password'")
    cursor.execute("GRANT SELECT ON Db.detection TO 'grafanaReader'")
    cnx.commit()

    cnx.close()

def input_data(device_id, time, temperature, wind, humidity, clouds, sensor_trigger):
    cnx, cursor = connect()

    sql = "INSERT INTO detection (device_id, time, temperature, clouds, humidity, wind, sensor_trigger) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    val = (device_id, time, temperature, clouds, humidity, wind, sensor_trigger)
    cursor.execute(sql, val)

    cnx.commit()
    cnx.close()

def read_all_entrys():
    cnx, cursor = connect()
    cursor.execute("SELECT * FROM detection")
    result = cursor.fetchall()
    cnx.close()

    for x in result:
        print(x)

def delete_table():
    cnx, cursor = connect()
    cursor.execute("DROP TABLE detection")
    cnx.close()

try:
    print("cheking entrys")
    read_all_entrys()
except:
    create_table()
    print("new emty table created")
