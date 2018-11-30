import asyncio
import json
import websockets
import sqlite3
import os


async def consulta_variables(archivo):
    conn = sqlite3.connect('./'+archivo)
    c=conn.cursor()
    sql1="PRAGMA table_info('escrituras')"
    try:
        c.execute(sql1)
        data_1=c.fetchall()
        variables=[a[1] for a in data_1]
    except sqlite3.DatabaseError:
        variables=[]   
    mensaje = json.dumps({'type': 'data', 'variables': variables})
    await notify_variables(mensaje)
    
variables={}    
USERS = set()
def archivos_en_raiz():
    files = os.listdir('./')
    archivos=[n for n in files if '.db' in n]
    return archivos

async def consulta_db(archivo,variable):
    try:
        conn = sqlite3.connect('./'+archivo)
        c=conn.cursor()        
        c.execute("SELECT "+variable+" FROM escrituras;")
        datos=c.fetchall()
        dic_datos={variable:datos}      
    except:
        datos_lista_nombres=''
        print("no hay fuentes") 
        dic_datos={}
        datos=''
    mensaje = json.dumps({'type': 'resultados', 'variable':variable ,'datos': datos})
    await notify_variables(mensaje)

def archivos_event():
    archivos=archivos_en_raiz()
    return json.dumps({'type': 'data', 'archivos': archivos})

def datos_event():
    return json.dumps({'type': 'data', nombre_variable : datos})

async def notify_variables(mensaje):
    if USERS:
        await asyncio.wait([user.send(mensaje) for user in USERS])

async def notify_datos():
    if USERS:       # asyncio.wait doesn't accept an empty list
        message = datos_event()
        await asyncio.wait([user.send(message) for user in USERS])

async def notify_archivos():
    if USERS:
        message = archivos_event()
        await asyncio.wait([user.send(message) for user in USERS])

async def register(websocket):
    ARCHIVOS={}
    USERS.add(websocket)
    await notify_archivos()

async def unregister(websocket):
    USERS.remove(websocket)
    await notify_archivos()

async def counter(websocket, path):
    await register(websocket)   #cuando se conecta le mando los nombres de los archivos dic archivos:nombres
    # usa notify_archivos
    try:
        #await websocket.send(archivos_event())
        async for message in websocket:
            data = json.loads(message)  #recibo mensaje
            
            #archivo=data.pop('archivo')
            if 'variable' in data.keys() and data['variable']!='' and 'archivo' in data.keys() and data['archivo']!='' : # si
                await consulta_db(data['archivo'],data['variable'])
            elif 'archivo' in data.keys() and data['archivo']!='':  # si recibo archivo
                await consulta_variables(data['archivo']) # creo dic varables:nombres
    finally:
        await unregister(websocket)

    

a=asyncio.get_event_loop().run_until_complete(websockets.serve(counter, 'localhost', 4200))
asyncio.get_event_loop().run_forever()