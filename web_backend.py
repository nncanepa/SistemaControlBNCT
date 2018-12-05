import asyncio
import json
import websockets
import sqlite3

## Se crea conexion a la base de datos
conn = sqlite3.connect('./base_de_datos_acelerador.db')
c = conn.cursor()
# Estado actual de cada fuente
STATE = {}
# Set de usuarios conectados a la interfaz
USERS = set()


def consulta_db():
    '''
    Consulto a la base de datos los valores de tension/corriente de las
    fuentes para devolverle a la interfaz
    '''
    try:
        # consulta de nombres de columnas
        sql1 = "PRAGMA table_info('escrituras')"
        c.execute(sql1)
        data_1 = c.fetchall()
        nombres_db = [a[1] for a in data_1]
        nombres = nombres_db
        lista_nombres = ','.join(nombres)
        
        # consulto ultimas tensiones cuadrupolos de arriba
        try:
            c.execute("SELECT " + lista_nombres + " FROM escrituras WHERE _rowid_ = (SELECT MAX(_rowid_) FROM escrituras);")
            datos_lista_nombres = c.fetchone()
        except:
            datos_lista_nombres = ''
            print("no hay fuentes")
        dic_datos = dict(zip(nombres, datos_lista_nombres))
    except:
        print("entro al except")
        dic_datos = {}
    return dic_datos


def state_event():
    '''
    Crea un json consultando a la base de datos.
    '''
    datos_tension = consulta_db()
    return json.dumps(datos_tension)


def users_event():
    '''
    Registra que un usuario nuevo se conecto a la interfaz
    '''
    return json.dumps({'type': 'users', 'count': len(USERS)})


async def notify_state():
    '''
    Notifica a todos los usuarios conectados sobre el estado actual
    de todas las fuentes
    '''
    if USERS:       # asyncio.wait doesn't accept an empty list
        message = state_event()
        await asyncio.wait([user.send(message) for user in USERS])


async def notify_users():
    '''
    Notifica a todos los usuarios la cantidad actual de usuarios
    conectados a la interfaz
    '''
    if USERS:       # asyncio.wait doesn't accept an empty list
        message = users_event()
        await asyncio.wait([user.send(message) for user in USERS])


async def register(websocket):
    '''
    Agrega al usuario recien conectado a la lista
    de usuarios conectados.
    '''
    USERS.add(websocket)
    await notify_users()


async def unregister(websocket):
    '''
    Quita un usuario de la lista de usuarios registrados.
    '''
    USERS.remove(websocket)
    await notify_users()


async def counter(websocket, path):
    await register(websocket)
    try:
        await websocket.send(state_event())
        async for message in websocket:
            data = json.loads(message)
            await notify_state()            
    finally:
        await unregister(websocket)

# Largamos el el loop principal de asyncio
a = asyncio.get_event_loop().run_until_complete(websockets.serve(counter, 'localhost', 4000))
asyncio.get_event_loop().run_forever()