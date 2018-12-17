import json
import paho.mqtt.client as mqtt
import websockets
import datetime
import sqlite3
import asyncio
import threading
from clases_esp.configESP import placa_0, placa_1, placa_2, placa_3, placa_4, placa_5, placa_6, placa_7, placa_8, placa_9

##########EN PLACAS VAN LAS INSTANCIAS CREADAS QUE SE QUIERAN UTILIZAR ########

placas = [placa_0, placa_1, placa_2, placa_3, placa_4, placa_5, placa_6, placa_7, placa_8, placa_9]
global tiempo_sms
tiempo_sms = datetime.datetime.now()

################### CONFIGURACION BASE DE DATOS ###############################
# conectarse a la base de datos


def insertar(que, donde):
    '''
    Funcion para insertar valores facilmente en la base de datos.
    '''
    conn = sqlite3.connect('./base_de_datos_acelerador.db')
    cursor = conn.cursor()
    columns =', '.join(que)
    placeholders = ', '.join('?' * len(que))
    sql = 'INSERT INTO '+donde+' ({}) VALUES ({})'.format(columns,
                                                          placeholders)
    cursor.execute(sql, tuple(que.values()))
    conn.commit()
    conn.close()


def initTablas(placas):
    '''
    Funcion que chequea si existen las tablas necesarias,
    si no existen las crea.
    '''
    conn = sqlite3.connect('./base_de_datos_acelerador.db')
    curr = conn.cursor()
    curr.execute("SELECT name FROM sqlite_master WHERE type='table';")
    # Si no tiene tablas crear tabla acelerador
    if not curr.fetchall(): 
        curr.execute('CREATE TABLE acelerador (fuente text,mac text)')
        h={}
        for placa in placas:
            for f in placa.lista_fuentes:
                h['fuente']=f
                h['mac']='No inplementado aun'
                insertar(h,'acelerador')
    try:
        # Intento leer tabla escrituras si no puedo la creo
        curr.execute("SELECT * FROM escrituras;") 
    except: 
        # Crear tabla de escrituras
        s='(tiempo text,'
        for placa in placas:
            for param_lec in placa.variables_lectura:
                # s = s + placa.variables_lectura[param_lec] + ' text,'
                s = s + param_lec + ' text,'
            for param_esc in placa.variables_escritura.keys():
                s = s + param_esc + ' text,'
        s = s[:-1]+')'
        print(s)
        curr.execute('CREATE TABLE escrituras ' + s)
    finally:
        conn.commit()
        conn.close()

# Inicializo la base de datos.


initTablas(placas)

################## FIN CONFIGURACION BASE DE DATOS ############################


def escritura_db():
    '''
    Esta funcion es llamada por el on_message del mqtt para guardar los datos.
    Escribe en la base de datos cuando recibo algun mensaje de una placa.
    '''
    dic_vals = {'tiempo': str(datetime.datetime.now().isoformat())}
    sdic_vals = {}
    # Leo los ultimos valores de las placas y creo un diccionario
    for placa in placas:
        dic_vals.update(placa.ultimo_lec)
        dic_vals.update(placa.ultimo_esc)
    # Convierto los valores a string
    for j in dic_vals:
        sdic_vals.update({j: str(dic_vals[j])})
    # Inserto los valores en la base de datos
    
    insertar(sdic_vals, 'escrituras')
###############################################################################
    
###################### escrutura clasica del websocket ########################


STATE = {'fuente': '',
         'accion': '',
         'valorv': 0,
         'valort': 0,
         'encendido': False}

USERS = set()

# Modificada para mandar el estado actual


async def register(websocket):
    USERS.add(websocket)
    # Cuando un usuario se conecta le envia la info de las placas
    for placa in placas:
        for f in placa.lista_fuentes:
            STATE['fuente'] = f
            try:
                STATE['valorv'] = placa.ultimo_esc[f+'_setV']
            except:
                pass
            try:
                STATE['encendido'] = placa.ultimo_esc[f+'_setO']
            except:
                pass
            STATE['accion'] = 'set'
            await notify_state()
    await notify_users()


def users_event():
    return json.dumps({'type': 'users', 'count': len(USERS)})


def state_event():
    return json.dumps({'type': 'state', **STATE})


async def notify_state():
    # asyncio.wait doesn't accept an empty list
    if USERS:
        message = state_event()
        await asyncio.wait([user.send(message) for user in USERS])


async def notify_users():
    # asyncio.wait doesn't accept an empty list
    if USERS:
        message = users_event()
        await asyncio.wait([user.send(message) for user in USERS])


async def unregister(websocket):
    USERS.remove(websocket)
    await notify_users()    
###############################################################################

######################## ##hilo principal del websocket #######################
# Aca esta el codigo que interpreta los mensajes de la pagina


async def hilo_del_ws(websocket, path):
    await register(websocket)
    try:
        # Wspero mensajes de la pagina
        async for message in websocket:
            # recibo mensaje de la pagina
            sms = json.loads(message)
            if sms['accion'] == 'actualizar':
                for placa in placas:
                    # Creo el mensaje para la placa
                    sms_topic, sms_txt = placa.set_valores(placa.ultimo_esc)
                    
                    # Publico el mensaje en el broker mqtt
                    mqttc.publish(sms_topic, sms_txt)
            else:
                # me fijo sobre que placa esp se quiere actuar
                for placa in placas:
                    if sms['fuente'] in placa.lista_fuentes:
                        placa_select = placa
                # Para la placa seleccionada me fijo que accion debe realizar
                ##
                # Eubir o bajar fuente (el signo del paso hace que suba o baje)
                if sms['accion'] == 'paso':
                    placa_select.ultimo_esc[sms['fuente'] + '_setV'] += sms['paso']
                # eEto cambia el estado de la fuente entre prendido y apagado
                if sms['accion']=='cambiar':
                    placa_select.ultimo_esc[sms['fuente'] + '_setO'] = \
                                            round(1 - placa_select.ultimo_esc[sms['fuente'] + '_setO'])
                
                # falta implementar rampas
                #if sms['accion']=='rampa':
                    #placa_select.ultimo_esc[sms['fuente']+'_setO']+=round(1-placa_select.ultimo_esc[sms['fuente']+'_setO'])

                # Directamente manda el valor enviado por la pagina a la placa
                if sms['accion'] == 'setear':
                    placa_select.ultimo_esc[sms['fuente'] + '_setV'] = sms['valorv']

                # Envio a la pagina los valores actualizados de la fuente que se modificaron
                STATE['fuente'] = sms['fuente']
                STATE['valorv'] = placa_select.ultimo_esc[sms['fuente'] + '_setV']
                STATE['encendido']=placa_select.ultimo_esc[sms['fuente'] + '_setO']
                # Esto le indica a la pagina que debe actualizar los valores
                STATE['accion'] = 'set'
                # Creo el mensaje para la placa
                sms_topic, sms_txt = placa_select.set_valores(placa_select.ultimo_esc)
                # Publico el mensaje en el broker mqtt
                mqttc.publish(sms_topic, sms_txt)
                
            await notify_state()
    finally:
        await unregister(websocket)
#############################################################################################


########################## comunicacion con el broker mqtt ##################################
def on_message(mqttc, obj, msg):
    global tiempo_sms
    tiempo_comparar = datetime.datetime.now()-datetime.timedelta(seconds=1.5)
    
    for placa in placas: # para todas las placas
        if placa.ultimo_tiempo < tiempo_comparar: # veo si hace mas de 1.5 seg no recibe mensajes
            for  v in placa.ultimo_lec.keys(): # escribo error como ultimo valor leido
                placa.ultimo_lec[v] = 'error'
            
        if msg.topic in placa.topic_lec: # si el topic es de la placa defino que voy a actuar sobre ella
            placa_select = placa
            placa_select.ultimo_tiempo = datetime.datetime.now() # actualizo el tiempo del ultimo mensaje recibido
        

    placa_select.get_valores(msg) # obtengo los valores
    tiempo_comparar = datetime.datetime.now() - datetime.timedelta(seconds = .1)
    if tiempo_sms < tiempo_comparar: # si paso mas de .1 seg desde la ultima escritura a la base de datos 
        tiempo_sms = datetime.datetime.now()
        escritura_db() # escribo en la base de datos


server = "192.168.1.100"
mqttc = mqtt.Client()
mqttc.connect(server, 1883, 60)
mqttc.on_message = on_message
for placa in placas:
    mqttc.subscribe(placa.topic_lec, 0)
mqttc.loop_start()
print("mqtt activo")
###############################################################################
#############################################################################################
import webbrowser, os
def iniciar_lecturas_continuo():
    os.system('web_backend.py')
def iniciar_lecturas_db():
    os.system('web_db.py')

filename='./html/interfaz_db.html'
webbrowser.open('file://' + os.path.realpath(filename))

filename='./html/panel_de_control_web.html'
webbrowser.open('file://' + os.path.realpath(filename))

t2=threading.Thread(target=iniciar_lecturas_continuo)
t2.daemon = True
t2.start()

t3=threading.Thread(target=iniciar_lecturas_db)
t3.daemon = True
t3.start()   
################################## definicion del websoket ####################
start_server = websockets.serve(hilo_del_ws, 'localhost', 6600)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
###############################################################################
###############################################################################
#############################################  FIN  ###########################
###############################################################################
###############################################################################