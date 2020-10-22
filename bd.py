import sqlite3
import pathlib
import requests as req
from math import sin, cos, sqrt, atan2, radians
from datetime import datetime
from sqlite3 import Error

pathAbs = pathlib.Path().absolute()
IDun = 1  #Puede cambiar

################################################################
###################### FUNCIONES BD ############################
################################################################

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn

def crear_tablas(conn):
    sql = '''CREATE TABLE IF NOT EXISTS coordenadas (
        id integer PRIMARY KEY AUTOINCREMENT,
        latitud NUMERIC NOT NULL,
        longitud NUMERIC NOT NULL,
        kilometraje NUMERIC NOT NULL,
        fecha TEXT NOT NULL);'''
    sql2 = '''CREATE TABLE IF NOT EXISTS pasajes (
        id integer PRIMARY KEY AUTOINCREMENT,
        token TEXT NOT NULL,
        idEntidadOperador INTEGER NOT NULL,
        idvuelta INTEGER NOT NULL,
        idunidad INTEGER NOT NULL);'''
    sql3 = '''CREATE TABLE IF NOT EXISTS pasajeserror (
        id integer PRIMARY KEY AUTOINCREMENT,
        token TEXT NOT NULL,
        idEntidadOperador INTEGER NOT NULL,
        idvuelta INTEGER NOT NULL,
        idunidad INTEGER NOT NULL);'''
    sql4 = '''CREATE TABLE IF NOT EXISTS pasajesefectivo (
        id integer PRIMARY KEY AUTOINCREMENT,
        idPasaje INTEGER NOT NULL,
        idvuelta INTEGER NOT NULL,
        idunidad INTEGER NOT NULL,
        monto NUMERIC NOT NULL,
        nropasajeros INTEGER NOT NULL,
        fecha TEXT NOT NULL,
        mensaje TEXT NOT NULL);'''
    sql5 = '''CREATE TABLE IF NOT EXISTS ajustes (
        id integer PRIMARY KEY AUTOINCREMENT,
        idunidad INTEGER NOT NULL,
        tiempo NUMERIC NOT NULL,
        varconfig TEXT NOT NULL);'''
    sql6 = '''CREATE TABLE IF NOT EXISTS posicion (
        latitud NUMERIC NOT NULL,
        longitud NUMERIC NOT NULL);'''
    cur = conn.cursor()
    cur.execute(sql)
    cur.execute(sql2)
    cur.execute(sql3)
    cur.execute(sql4)
    cur.execute(sql5)
    cur.execute(sql6)
    conn.commit()    

def nueva_coordenada(conn, coordenada):
    """
    Crea una coordenada en coordenadas
    :param latitud:
    :param longitud:
    :param kilometraje:
    :param fecha:
    :return: project id
    """
    sql = ''' INSERT INTO coordenadas(latitud,longitud,kilometraje,fecha)
              VALUES(?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, coordenada)
    conn.commit()
    return cur.lastrowid

def eliminar_coordenadas(conn):
    """
    Elimina todo en coordenadas
    """

    sql = ''' DELETE FROM coordenadas'''
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()

def listar_coordenada(conn):
    sql = ''' SELECT latitud,longitud,kilometraje,fecha FROM coordenadas '''
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    return rows

def nuevo_pasaje(conn, pasaje):
    """
    Crea un nuevo pasaje en pasajes
    :param token:
    :param idoperador:
    :param idvuelta:
    :param idunidad:
    :return: pasajes id
    """
    sql = ''' INSERT INTO pasajes(token,idEntidadOperador,idvuelta,idunidad)
              VALUES(?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, pasaje)
    conn.commit()
    return cur.lastrowid

def eliminar_pasajes(conn):
    """
    Elimina todo en pasajes
    """

    sql = ''' DELETE FROM pasajes'''
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()

def listar_pasajes(conn):
    sql = ''' SELECT token,idEntidadOperador,idvuelta,idunidad FROM pasajes '''
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    return rows

def nuevo_pasaje_efectivo(conn, pasajeEfectivo):
    """
    Crea un nuevo pasaje en pasajesefectivo
    :param idPasaje:
    :param idvuelta:
    :param idunidad:
    :param monto:
    :param nropasajeros:
    :param fecha:
    :param mensaje:
    :return: pasajesefectivo id
    """
    sql = ''' INSERT INTO pasajesefectivo(idPasaje,idvuelta,idunidad,monto,nropasajeros,fecha,mensaje)
              VALUES(?,?,?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, pasajeEfectivo)
    conn.commit()
    return cur.lastrowid

def eliminar_pasajes_efectivo(conn):
    """
    Elimina todo en pasajesefectivo
    """

    sql = ''' DELETE FROM pasajesefectivo'''
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()

def listar_pasajes_efectivos(conn):
    sql = ''' SELECT idPasaje,idvuelta,idunidad,monto,nropasajeros,fecha,mensaje FROM pasajesefectivo '''
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    return rows

def nuevo_ajuste(conn,datos):
    cur = conn.cursor()
    sql = "SELECT Count() FROM ajustes"
    cur.execute(sql)
    cantidadRow = cur.fetchone()[0]
    if(cantidadRow == 0):
        sql = " INSERT INTO ajustes(idunidad,tiempo,varconfig) VALUES (?,?,?) "
    else:
        sql = " UPDATE ajustes SET idunidad = ? , tiempo = ? , varconfig = ? "
    cur.execute(sql,datos)
    conn.commit()

def listar_ajustes(conn):
    sql = ''' SELECT idunidad,tiempo,varconfig FROM ajustes '''
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchone()
    return rows

def nuevo_pasaje_error(conn,datos):
    """
    Crea un nuevo pasaje en pasajes
    :param token:
    :param idoperador:
    :param idvuelta:
    :param idunidad:
    :return: pasajes id
    """
    sql = ''' INSERT INTO pasajeserror(token,idEntidadOperador,idvuelta,idunidad)
              VALUES(?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, datos)
    conn.commit()
    return cur.lastrowid

def eliminar_pasaje_error(conn):
    """
    elimina un nuevo pasaje en pasajeserror
    """
    sql = ''' DELETE FROM pasajeserror '''
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()

def listar_pasaje_error(conn):
    """
    Enlista pasajes en pasajeserror
    """
    sql = ''' SELECT token,idEntidadOperador,idvuelta,idunidad FROM pasajeserror '''
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    return rows

def nueva_posicion(conn,datos):
    cur = conn.cursor()
    sql = "SELECT Count() FROM posicion"
    cur.execute(sql)
    cantidadRow = cur.fetchone()[0]
    if(cantidadRow == 0):
        sql = " INSERT INTO posicion(latitud,longitud) VALUES (?,?) "
    else:
        sql = " UPDATE posicion SET latitud = ? , longitud = ? "
    cur.execute(sql,datos)
    conn.commit()

def eliminar_posicion(conn):
    sql = ''' DELETE FROM posicion '''
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()

def listar_posicion(conn):
    sql = ''' SELECT * FROM posicion '''
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchone()
    return rows

################################################################
###################### FUNCIONES WS ############################
################################################################


def cobrarUnPasaje(m_token):
  pasaje = {'token': m_token,'idEntidadOperador': 0 ,'idvuelta': 0,'idunidad': IDun}

  hed = {'Content-type': 'application/json', 'Accept': 'text/plain'}
  url = 'http://desarrollo.sreasons.com:8081/MSOperacionesBusCommand/api/v1/'

  response2 = req.post(url+'cobros', headers=hed, json = pasaje)
  print(response2.json())
  if (response2.status_code==200):
    return "OK"
  else:
    return "ERROR"

def cobrarVariosPasajes(conn):
  pasajes_varios = []
  rows = listar_pasajes(conn)
  for row in rows:
      pasaje = { "token": row[0],"idEntidadOperador": row[1],"idvuelta": row[2],"idunidad": row[3]}
      pasajes_varios.append(pasaje)

  if(len(pasajes_varios)==0):
    return

  hed = {'Content-type': 'application/json', 'Accept': 'text/plain'}
  url = 'http://desarrollo.sreasons.com:8081/MSOperacionesBusCommand/api/v1/'

  response2 = req.post(url+'multicobros', headers=hed, json = pasajes_varios)

  if (response2.status_code==200):
    respuestas = response2.json()
    for respuesta in respuestas:
        if(respuesta['mensaje'] != 'COBRO EXITOSO'):
            dat = rows[respuestas.index(respuesta)]
            datos = (dat[0],dat[1],dat[2],dat[3])
            nuevo_pasaje_error(conn,datos)
    eliminar_pasajes(conn)
    return "OK"
  else:
    return "ERROR"

def obtenerMinutos(IdVar):
  parametros = {'idunidad': IdVar}

  #hed = {'Content-type': 'application/json', 'Accept': 'text/plain'}
  url = 'http://desarrollo.sreasons.com:8081/MSOperacionesBusQuery/api/v1/unidades/'

  response2 = req.get(url+'minutosoffline', params = parametros)

  if (response2.status_code==200):
    return response2.json()
  else:
    return "ERROR"

def coordenadasOnline(latitud,longitud,kilometraje):
  coordenada = [{"idUnidad": IDun, "latitud" :latitud,  "longitud": longitud ,"kilometraje":kilometraje , "fecha": str(datetime.now())}]

  hed = {'Content-type': 'application/json', 'Accept': 'text/plain' , 'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6IjY2MDM3MzJFMzIyN0MwN0JFOEQwQUJENDcyRjM4NTBBOEYzNDRFRkQiLCJ0eXAiOiJKV1QifQ.eyJuYmYiOjE2MDA0NTY2MTgsImV4cCI6MTYwMDU0Mjc3OCwiaXNzIjoibXNzZWd1cmlkYWRhcHBzIiwiYXVkIjoiMjdlODZjNGM0NGVkNGQwMTgwOWMyNDA1MTZlZGZkYzEiLCJzY29wZXMiOnsiSWRVc3VhcmlvIjoxMDAyNCwiVXN1YXJpbyI6InJheTI3N0BnbWFpbC5jb20iLCJUaXBvVG9rZW4iOjMsIklkRW50aWRhZFBlcnNvbmEiOjEwMDU5LCJJZEVudGlkYWRFbXByZXNhIjoxLCJJZEludml0YWRvIjoyNzAsIkRhdG8xIjpudWxsLCJEYXRvMiI6bnVsbCwiRGF0bzMiOm51bGwsIlN1Y3Vyc2FsZXMiOltdLCJTZXJ2aWNpb3MiOlsxMDAsMTAxLDEwMiwxMDMsMTA0LDEwNSwxMDYsMTA3LDEwOCwxMDksMTEwLDExMSwxMTIsMTEzLDE0MSwxNDIsMTQzLDE0NiwxNDcsMTQ4XX19.BReyRhl5sMPQii_HyczZAN0YNfoZ9rAwKLGDCFqbsWwFAy0NN4kC4WamT2EwaERy77VOQkaUe720O8NJ8foXmqGoD116PPv8MpZ51L4FPT1pACvK8aiDyaRsS47E5d5mA1vH3Hn3NmjIzF-ig-NaNlQLRwrA1z8AcOURebJ7L5xkcANzeOcKAFIrvdXV5Kq7La4Zfz4L-wup4guKs87wDTDvIIZ2yZms5WTZEazx0UJUuzL0-l5PJgbYnKpH4cbhSC3hgrh2aLFdJVMzmRR8C-xGVGXvq9-mfRgs_CzzwqIlUTMHH8exPMJlirw6hUJ3Gr6RAPoqoDT50B2oqCdy8A'}
  url = 'http://desarrollo.sreasons.com:8081/MSGestionBuscommand/api/v1/'

  response2 = req.post(url+'coordenadas', headers=hed, json = coordenada)

  if (response2.status_code==200):
    return response2.json()
  else:
    return "ERROR"

def coordenadasOffline(conn):
  coordenadas = []
  rows = listar_coordenada(conn)
  for row in rows:
      coordenada = {"idUnidad": IDun,"latitud": row[0],"longitud": row[1],"kilometraje": row[2],"fecha": row[3]}
      coordenadas.append(coordenada)
  
  if(len(coordenadas)==0):
    return

  hed = {'Content-type': 'application/json', 'Accept': 'text/plain' , 'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6IjY2MDM3MzJFMzIyN0MwN0JFOEQwQUJENDcyRjM4NTBBOEYzNDRFRkQiLCJ0eXAiOiJKV1QifQ.eyJuYmYiOjE2MDA0NTY2MTgsImV4cCI6MTYwMDU0Mjc3OCwiaXNzIjoibXNzZWd1cmlkYWRhcHBzIiwiYXVkIjoiMjdlODZjNGM0NGVkNGQwMTgwOWMyNDA1MTZlZGZkYzEiLCJzY29wZXMiOnsiSWRVc3VhcmlvIjoxMDAyNCwiVXN1YXJpbyI6InJheTI3N0BnbWFpbC5jb20iLCJUaXBvVG9rZW4iOjMsIklkRW50aWRhZFBlcnNvbmEiOjEwMDU5LCJJZEVudGlkYWRFbXByZXNhIjoxLCJJZEludml0YWRvIjoyNzAsIkRhdG8xIjpudWxsLCJEYXRvMiI6bnVsbCwiRGF0bzMiOm51bGwsIlN1Y3Vyc2FsZXMiOltdLCJTZXJ2aWNpb3MiOlsxMDAsMTAxLDEwMiwxMDMsMTA0LDEwNSwxMDYsMTA3LDEwOCwxMDksMTEwLDExMSwxMTIsMTEzLDE0MSwxNDIsMTQzLDE0NiwxNDcsMTQ4XX19.BReyRhl5sMPQii_HyczZAN0YNfoZ9rAwKLGDCFqbsWwFAy0NN4kC4WamT2EwaERy77VOQkaUe720O8NJ8foXmqGoD116PPv8MpZ51L4FPT1pACvK8aiDyaRsS47E5d5mA1vH3Hn3NmjIzF-ig-NaNlQLRwrA1z8AcOURebJ7L5xkcANzeOcKAFIrvdXV5Kq7La4Zfz4L-wup4guKs87wDTDvIIZ2yZms5WTZEazx0UJUuzL0-l5PJgbYnKpH4cbhSC3hgrh2aLFdJVMzmRR8C-xGVGXvq9-mfRgs_CzzwqIlUTMHH8exPMJlirw6hUJ3Gr6RAPoqoDT50B2oqCdy8A'}
  url = 'http://desarrollo.sreasons.com:8081/MSGestionBuscommand/api/v1/'

  response2 = req.post(url+'coordenadas', headers=hed, json = coordenadas)

  if (response2.status_code==200):
    return response2.json()
  else:
    return "ERROR"

def cobrarEfectivo(monto):
  pasajes_varios = [{"idPasaje": 0,"idVuelta": 0,"idunidad": IDun,"monto": monto,"nropasajeros": 0,"fecha": str(datetime.now()),"mensaje": ""}]

  hed = {'Content-type': 'application/json', 'Accept': 'text/plain', 'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6IjY2MDM3MzJFMzIyN0MwN0JFOEQwQUJENDcyRjM4NTBBOEYzNDRFRkQiLCJ0eXAiOiJKV1QifQ.eyJuYmYiOjE2MDMyMjU0NjUsImV4cCI6MTYwMzMxMTYyNSwiaXNzIjoibXNzZWd1cmlkYWRhcHBzIiwiYXVkIjoiYzYzNzUyMmNlNTIxNDQyNDhlYmQyMmZkYmI2YzFkZWMiLCJzY29wZXMiOnsiSWRVc3VhcmlvIjoyMTYsIlVzdWFyaW8iOiJqdWNoYW1hY29AZ21haWwuY29tIiwiVGlwb1Rva2VuIjozLCJJZEVudGlkYWRQZXJzb25hIjoyNTcsIklkRW50aWRhZEVtcHJlc2EiOjEsIklkSW52aXRhZG8iOjI0MCwiRGF0bzEiOm51bGwsIkRhdG8yIjpudWxsLCJEYXRvMyI6bnVsbCwiU3VjdXJzYWxlcyI6W10sIlNlcnZpY2lvcyI6WzE0NF19fQ.PvXIeca34G2bYgyU9nqRZosDVol9pAvXERaDce88iPehkUl5mjLEbEWEtV0HQ0PXXbfm4uhdqYb8mFUpigWWpm9m1ik6Q2ZnOF9xNGavKnIdVWavhXKsNVZAClmzQyZOvvxx2CP9qi90DKPdqDWCZ10KJsgo4bk1IdRa_EGLFpmfv83fEJ8PmYmQ8uDrl8saMvazdR7m-263QCDwSQH1IJellYb2_T2n6DKzZm8FDvJdtDtjoTJe-8i1BZJ-ijlrWEbg0WU6x2M57Wemp3p9sJJSONIrs892BsfN8CfF9TIVWpsD1L_T6GS2m5iuitauHY1DcJJpevi0e7hSAD7sUg'}
  url = 'http://desarrollo.sreasons.com:8081/MSOperacionesBusCommand/api/v1/'

  response2 = req.post(url+'multicobrosefectivo', headers=hed, json = pasajes_varios)

  print (response2.status_code)
  if (response2.status_code==200):
    return "OK"
  else:
    return "ERROR"

def cobrarEfectivoOffline(monto):
  pasajes_efectivo = []
  rows = listar_pasajes_efectivos(conn)
  for row in rows:
      pasaje = {"idPasaje": row[0],"idVuelta": row[1],"idunidad": row[2],"monto": row[3],"nropasajeros": row[4],"fecha": row[5],"mensaje": row[6]}
      pasajes_efectivo.append(pasaje)

  if(len(pasajes_efectivo)==0):
    return

  hed = {'Content-type': 'application/json', 'Accept': 'text/plain', 'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6IjY2MDM3MzJFMzIyN0MwN0JFOEQwQUJENDcyRjM4NTBBOEYzNDRFRkQiLCJ0eXAiOiJKV1QifQ.eyJuYmYiOjE2MDMyMjU0NjUsImV4cCI6MTYwMzMxMTYyNSwiaXNzIjoibXNzZWd1cmlkYWRhcHBzIiwiYXVkIjoiYzYzNzUyMmNlNTIxNDQyNDhlYmQyMmZkYmI2YzFkZWMiLCJzY29wZXMiOnsiSWRVc3VhcmlvIjoyMTYsIlVzdWFyaW8iOiJqdWNoYW1hY29AZ21haWwuY29tIiwiVGlwb1Rva2VuIjozLCJJZEVudGlkYWRQZXJzb25hIjoyNTcsIklkRW50aWRhZEVtcHJlc2EiOjEsIklkSW52aXRhZG8iOjI0MCwiRGF0bzEiOm51bGwsIkRhdG8yIjpudWxsLCJEYXRvMyI6bnVsbCwiU3VjdXJzYWxlcyI6W10sIlNlcnZpY2lvcyI6WzE0NF19fQ.PvXIeca34G2bYgyU9nqRZosDVol9pAvXERaDce88iPehkUl5mjLEbEWEtV0HQ0PXXbfm4uhdqYb8mFUpigWWpm9m1ik6Q2ZnOF9xNGavKnIdVWavhXKsNVZAClmzQyZOvvxx2CP9qi90DKPdqDWCZ10KJsgo4bk1IdRa_EGLFpmfv83fEJ8PmYmQ8uDrl8saMvazdR7m-263QCDwSQH1IJellYb2_T2n6DKzZm8FDvJdtDtjoTJe-8i1BZJ-ijlrWEbg0WU6x2M57Wemp3p9sJJSONIrs892BsfN8CfF9TIVWpsD1L_T6GS2m5iuitauHY1DcJJpevi0e7hSAD7sUg'}
  url = 'http://desarrollo.sreasons.com:8081/MSOperacionesBusCommand/api/v1/'

  response2 = req.post(url+'multicobrosefectivo', headers=hed, json = pasajes_efectivo)
  
  if (response2.status_code==200):
    return "OK"
  else:
    return "ERROR"
    

def dispositivo(conn,mac):
  parametros = {'macdispositivo': mac}

  hed = {'Content-type': 'application/json', 'Accept': 'text/plain', 'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6IjY2MDM3MzJFMzIyN0MwN0JFOEQwQUJENDcyRjM4NTBBOEYzNDRFRkQiLCJ0eXAiOiJKV1QifQ.eyJuYmYiOjE2MDMyMjU0NjUsImV4cCI6MTYwMzMxMTYyNSwiaXNzIjoibXNzZWd1cmlkYWRhcHBzIiwiYXVkIjoiYzYzNzUyMmNlNTIxNDQyNDhlYmQyMmZkYmI2YzFkZWMiLCJzY29wZXMiOnsiSWRVc3VhcmlvIjoyMTYsIlVzdWFyaW8iOiJqdWNoYW1hY29AZ21haWwuY29tIiwiVGlwb1Rva2VuIjozLCJJZEVudGlkYWRQZXJzb25hIjoyNTcsIklkRW50aWRhZEVtcHJlc2EiOjEsIklkSW52aXRhZG8iOjI0MCwiRGF0bzEiOm51bGwsIkRhdG8yIjpudWxsLCJEYXRvMyI6bnVsbCwiU3VjdXJzYWxlcyI6W10sIlNlcnZpY2lvcyI6WzE0NF19fQ.PvXIeca34G2bYgyU9nqRZosDVol9pAvXERaDce88iPehkUl5mjLEbEWEtV0HQ0PXXbfm4uhdqYb8mFUpigWWpm9m1ik6Q2ZnOF9xNGavKnIdVWavhXKsNVZAClmzQyZOvvxx2CP9qi90DKPdqDWCZ10KJsgo4bk1IdRa_EGLFpmfv83fEJ8PmYmQ8uDrl8saMvazdR7m-263QCDwSQH1IJellYb2_T2n6DKzZm8FDvJdtDtjoTJe-8i1BZJ-ijlrWEbg0WU6x2M57Wemp3p9sJJSONIrs892BsfN8CfF9TIVWpsD1L_T6GS2m5iuitauHY1DcJJpevi0e7hSAD7sUg' }
  url = 'http://desarrollo.sreasons.com:8081/MSGestionBusQuery/api/v1/'

  response2 = req.get(url+'dispositivos', headers=hed , params = parametros)

  if (response2.status_code==200):
    IdVar = response2.json()
    minutos = obtenerMinutos(IdVar)
    if minutos:
        datos = (IdVar,minutos,"")
        print(datos)
        nuevo_ajuste(conn,datos)
        return "OK"
    return "NO MINUTOS"
  else:
    return "ERROR"

def distancia2puntos(conn,latitud,longitud):

  R = 6378.1
  row = listar_posicion(conn)

  lat1 = radians(row[0])
  lon1 = radians(row[1])
  lat2 = radians(latitud)
  lon2 = radians(longitud)

  dlon = lon2 - lon1
  dlat = lat2 - lat1

  a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
  c = 2 * atan2(sqrt(a), sqrt(1 - a))

  return round(R * c,2) #redondear a 2 digitos

################################################################
###################### OPERACIONES  ############################
################################################################

database = r"%s\pythonsqlite.db"%pathAbs
conn = create_connection(database)
crear_tablas(conn)

print('*******************  dispositivo  ********************')
print(dispositivo(conn,"dc:a6:32:97:93:67"))

print(listar_ajustes(conn))
nueva_posicion(conn,(0,0))

print(str(datetime.now()))
print('*******************  distancia inicio  ********************')
print(distancia2puntos(conn,52.2296756,21.0122287))
nueva_posicion(conn,(52.2296756,21.0122287))
print('*******************  distancia nueva   ********************')
print(distancia2puntos(conn,52.406374,16.9251681))

print('*******************  cobroEfectivo  ********************')
print(cobrarEfectivo(1.50))

#print('**************minutosUnidad*****************')
#print(obtenerMinutos(conn))

#print('**************coordenadasOnline*****************')
#print(coordenadasOnline(-1.398951, -1.536827, 1234.56))

#print('**************coordenadasOffline*****************')
#print(coordenadasOffline2())

#print('**************PASAJE UNICO*****************')
#pasaje = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzY29wZSI6eyJJZHBhc2FqZSI6MTEwNzQsIklkZW50aWRhZCI6MTUxLCJNb250byI6MS4wLCJ0aXBvVG9rZW4iOjF9LCJleHAiOjYzOTE3MDk5MzQzLCJpYXQiOjYzNzM3MDk5MzQzfQ.SMs1YDHJAkGoySqIBW0JQgJPTQ0YfDWRAc9vZM5xLqY'
#print(cobrarUnPasaje(pasaje))

#datos = (pasaje,0,0,IDun)
#nuevo_pasaje(conn,datos)
#nuevo_pasaje(conn,datos)

#print('**************PASAJES VARIOS***************')
#print(cobrarVariosPasajes(conn))

#print('**************PASAJES ERROR***************')
#rows = listar_pasaje_error(conn)
#for row in rows:
#    print(row)