import json
import paho.mqtt.client as mqtt
import threading
import websockets
import time
import datetime
import sqlite3
import os
import asyncio
import websockets
from clases_esp.espClass import esp
from clases_esp.configESP import *

##################EN PLACAS VAN LAS INSTANCIAS CREADAS QUE SE QUIERAN UTILIZAR #################

placas=[placa_1,placa_2,placa_3,placa_4,placa_5,placa_9]
global tiempo_sms
tiempo_sms=datetime.datetime.now()
dt=datetime.timedelta(seconds=0.2)

################################ CONFIGURACION BASE DE DATOS ####################################
# conectarse a la base de datos

conn = sqlite3.connect('./base_de_datos_acelerador.db')
curr = conn.cursor()

def insertar(que,donde):
    '''
    Funcion para insertar valores facilmente en la base de datos.
    '''
    conn = sqlite3.connect('./base_de_datos_acelerador.db')
    cursor = conn.cursor()    
    columns =', '.join(que)
    placeholders = ', '.join('?' * len(que))
    sql = 'INSERT INTO '+donde+' ({}) VALUES ({})'.format(columns, placeholders)
    cursor.execute(sql, tuple(que.values()))
    conn.commit()
    conn.close()

curr.execute("SELECT name FROM sqlite_master WHERE type='table';")
if not curr.fetchall(): # si no tiene tablas crear tabla acelerador
    curr.execute('CREATE TABLE acelerador (fuente text,mac text)')
    h={}
    for placa in placas:
        for f in placa.lista_fuentes:
            h['fuente']=f
            h['mac']='No inplementado aun'
            insertar(h,'acelerador')


try:
    curr.execute("SELECT * FROM escrituras;") #intento leer tabla escrituras si no puedo la creo
except: #crear tabla de escrituras
    s='(tiempo text,'
    for placa in placas:
        for param_lec in placa.variables_lectura:
            s=s+placa.variables_lectura[param_lec]+' text,'
    s=s[:-1]+')'
    print(s)
    curr.execute('CREATE TABLE escrituras '+s)

conn.commit()
conn.close()
############################# FIN CONFIGURACION BASE DE DATOS ####################################

def escritura_db():
    ''' 
    Esta funcion es llamada por el on_message del mqtt para guardar los datos.
    Escribe en la base de datos cuando recibo algun mensaje de una placa.
    '''
    dic_vals={'tiempo':str(datetime.datetime.now().isoformat())}
    sdic_vals={}
    for placa in placas: # leo los ultimos valores de las placas y creo un diccionario
        dic_vals.update(placa.ultimo_lec)   
    for j in dic_vals: #convierto los valores a string
        sdic_vals.update({j:str(dic_vals[j])})
    insertar(sdic_vals,'escrituras') # inserto los valores en la base de datos
######################################################################################
    
###################### escrutura clasica del websocket ###############################
STATE = {'fuente':'','accion':'','valorv': 0,'valort': 0,'encendido':False}
USERS = set()
async def register(websocket): # modificada para mandar el estado actual
    USERS.add(websocket)
    for placa in placas: # cuando un usuario se conecta le envia la info de las placas
        for f in placa.lista_fuentes:
            STATE['fuente'] = f
            try:
                STATE['valorv']  = placa.ultimo_esc[f+'_setV']
            except:
                pass
            try:
                STATE['encendido']  = placa.ultimo_esc[f+'_onoff']
            except:
                pass
            STATE['accion']  = 'set'
            await notify_state()
    await notify_users()

def users_event():
    return json.dumps({'type': 'users', 'count': len(USERS)})

def state_event():
    return json.dumps({'type': 'state', **STATE})

async def notify_state():
    if USERS:       # asyncio.wait doesn't accept an empty list
        message = state_event()
        await asyncio.wait([user.send(message) for user in USERS])
        
async def notify_users():
    if USERS:       # asyncio.wait doesn't accept an empty list
        message = users_event()
        await asyncio.wait([user.send(message) for user in USERS])
        
async def unregister(websocket):
    USERS.remove(websocket)
    await notify_users()    
#######################################################################################

######################## ##hilo principal del websocket ###############################
async def hilo_del_ws(websocket, path): # aca esta el codigo que intertreta los mensajes de la pagina
    await register(websocket)
    try:
        async for message in websocket: # espero mensajes de la pagina
            # recibo mensaje de la pagina
            sms=json.loads(message)
            
            if sms['accion']=='actualizar':
                for placa in placas:
                    sms_topic,sms_txt=placa.set_valores(placa.ultimo_esc) # creo el mensaje para la placa
                    mqttc.publish(sms_topic,sms_txt) # publico el mensaje en el broker mqtt                    
            else:
                # me fijo sobre que placa esp se quiere actuar
                for placa in placas:
                    if sms['fuente'] in placa.lista_fuentes:
                        placa_select=placa
                # para la placa seleccionada me fijo que accion debe realizar
                if sms['accion']=='paso': # subir o bajar fuente (el signo del paso hace que suba o baje)
                    placa_select.ultimo_esc[sms['fuente']+'_setV']+=sms['paso']
                if sms['accion']=='cambiar': # esto cambia el estado de la fuente entre prendido y apagado
                    placa_select.ultimo_esc[sms['fuente']+'_onoff']=round(1-placa_select.ultimo_esc[sms['fuente']+'_onoff'])
                
                # falta implementar rampas
                #if sms['accion']=='rampa':
                    #placa_select.ultimo_esc[sms['fuente']+'_onoff']+=round(1-placa_select.ultimo_esc[sms['fuente']+'_onoff'])
                
                if sms['accion']=='setear': # directamente manda el valor enviado por la pagina a la placa
                    placa_select.ultimo_esc[sms['fuente']+'_setV']=sms['valorv']
                
                # envio a la pagina los valores actualizados de la fuente que se modificaron
                STATE['fuente'] = sms['fuente']
                STATE['valorv']  = placa_select.ultimo_esc[sms['fuente']+'_setV']
                STATE['encendido']=placa_select.ultimo_esc[sms['fuente']+'_onoff']
                STATE['accion'] = 'set'            # esto le indica a la pagina que debe actualizar los valores
                sms_topic,sms_txt=placa_select.set_valores(placa_select.ultimo_esc) # creo el mensaje para la placa
                mqttc.publish(sms_topic,sms_txt) # publico el mensaje en el broker mqtt
                print(placa_select.ultimo_lec)
            await notify_state()
    finally:
        await unregister(websocket)
#############################################################################################


########################## comunicacion con el broker mqtt ##################################
def on_message(mqttc, obj, msg):
    global tiempo_sms
    tiempo_comparar=datetime.datetime.now()-datetime.timedelta(seconds=5)
    
    for placa in placas:
        if placa.ultimo_tiempo<tiempo_comparar:
            for  v in placa.ultimo_lec.keys():
                placa.ultimo_lec[v]='error'
            
        if msg.topic in placa.topic_lec:
            placa_select=placa
            placa_select.ultimo_tiempo=datetime.datetime.now()
        
    placa_select.get_valores(msg)
    tiempo_comparar=datetime.datetime.now()-datetime.timedelta(seconds=.2)
    if tiempo_sms<tiempo_comparar:
        tiempo_sms=datetime.datetime.now()
        escritura_db()
 
    
server = "192.168.1.100"
mqttc = mqtt.Client()
mqttc.connect(server, 1883, 60)
mqttc.on_message = on_message
for placa in placas:
    mqttc.subscribe(placa.topic_lec,0)
mqttc.loop_start()
#############################################################################################

################################## definicion del websoket ##################################        
start_server = websockets.serve(hilo_del_ws, 'localhost', 6600)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
#############################################################################################
#############################################################################################
#############################################  FIN  #########################################
#############################################################################################
#############################################################################################