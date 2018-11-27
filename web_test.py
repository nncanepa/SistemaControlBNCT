import asyncio
import json
import websockets
import sqlite3


conn = sqlite3.connect('./base_de_datos_acelerador.db')
c=conn.cursor()
STATE = {}
USERS = set()


def consulta_db():
    try:
        # consulta de nombres de columnas
        sql1="PRAGMA table_info('escrituras')"
        c.execute(sql1)
        data_1=c.fetchall()
        nombres_db=[a[1] for a in data_1]
        # separo nombres entre tensiones y corrientes
        #nombres=[n for n in nombres_db if '_getV' in n]
        #if 'Nivel_FAR_getI' in nombres_db: # agrego corriente en la copa de faraday a la consulta
            #nombres.append('Nivel_FAR_getI')
        nombres=nombres_db
        lista_nombres=','.join(nombres)
        
        # consulto ultimas tensiones cuadrupolos de arriba
        try:
            c.execute("SELECT "+lista_nombres+" FROM escrituras WHERE _rowid_ = (SELECT MAX(_rowid_)  FROM escrituras);")
            datos_lista_nombres=c.fetchone()
        except:
            datos_lista_nombres=''
            print("no hay fuentes")       
        dic_datos=dict(zip(nombres,datos_lista_nombres))
    except:
        print("entro al except")
        dic_datos={}
    #print(dic_datos)
    return dic_datos


def state_event():
    datos_tension=consulta_db()
    return json.dumps(datos_tension)


def users_event():
    return json.dumps({'type': 'users', 'count': len(USERS)})

async def notify_state():
    if USERS:       # asyncio.wait doesn't accept an empty list
        message = state_event()
        await asyncio.wait([user.send(message) for user in USERS])

async def notify_users():
    if USERS:       # asyncio.wait doesn't accept an empty list
        message = users_event()
        await asyncio.wait([user.send(message) for user in USERS])

async def register(websocket):
    USERS.add(websocket)
    await notify_users()

async def unregister(websocket):
    USERS.remove(websocket)
    await notify_users()

async def counter(websocket, path):
    await register(websocket)
    try:
        await websocket.send(state_event())
        async for message in websocket:
            data = json.loads(message)
            #if 'tensiones' in data.keys():
                #print('tensiones')
            #if 'corrientes' in data.keys():
                #print('corrientes')            
            await notify_state()            
    finally:
        await unregister(websocket)

    

a=asyncio.get_event_loop().run_until_complete(websockets.serve(counter, 'localhost', 4000))
asyncio.get_event_loop().run_forever()