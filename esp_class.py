import json
import paho.mqtt.client as mqtt
import threading
import websockets
import time
import datetime

class esp():
    def __init__(self):
        self.lista_lec={}
        self.lista_esc={}
        self.lista_fuentes=set()
        self.ultimo_esc={}
        self.ultimo_lec={}
        self.ultimo_tiempo=datetime.datetime.now()
        
    ##### asignar 0 a todos los valores de escritura de la placa #####
    def activar(self):
        for s in self.lista_esc:
            self.ultimo_esc[s]=0
             
    ##### asignar nombres externos de las fuentes que controla la placa #####
    def set_fuentes(self,lista):
        self.lista_fuentes.add(lista)
        
    ##### asignar nombres externos a las variables que lee la placa #####
    def set_variables_lectura(self,lista_variables):
        self.lista_lec.update(lista_variables)
        for j in lista_variables:
            self.ultimo_lec.update({lista_variables[j]:0})
        #for var in lista_variables:
            #setattr(self,lista_variables[var],var)
            
    ##### asignar nombres externos a las variables que escribe la placa #####        
    def set_variables_escritura(self,lista_variables):
        self.lista_esc.update(lista_variables)
        
    ##### asignar el topic de escritura de la placa #####
    def set_topic_esc(self,topic):
        self.topic_esc=topic
        
    ##### asignar el topic de lectura de la placa #####
    def set_topic_lec(self,topic):
        self.topic_lec=topic    
        
    ##### crea un mensaje para mandar al broker #####    
    def set_valores(self,valores):
        mensaje={}
        if len(valores)!=len(self.lista_esc):
            print('la cantidad de valores a setear es incorrecta')
            print('se esperan',len(self.lista_esc),'valores')
            print('se recibieron',len(valores),'valores')
        else:
            for datos in valores:
                if datos in self.lista_esc.keys():
                    mensaje[self.lista_esc[datos]]=valores[datos]
                    mensaje_completo=(self.topic_esc,str(mensaje))
                else:
                    print('lista de escritura incorrecta... utilice la funcion set_variables_escritura')
                    print('no se encontro la clave '+datos)
                    print(datos,valores[datos],'no asignado')
            return mensaje_completo
    
    ##### lee un mensaje que le manda el broker y guarda los datos dentro de la instancia con los nombres externos #####
    def get_valores(self,msg):
        check=True
        ultimo={}
        mensaje=json.loads(msg.payload)
        if len(mensaje)!=len(self.lista_lec):
            check=False
            print('la cantidad de valores leidos es incorrecta')
            print('se esperan',len(self.lista_lec),'valores')
            print('se recibieron',len(mensaje),'valores')            
        else:
            for datos in mensaje:
                if datos in self.lista_lec.keys():
                    #setattr(self,self.lista_lec[datos],mensaje[datos])
                    ultimo[self.lista_lec[datos]]=mensaje[datos]
                else:
                    check=False
                    print('lista de lectura incorrecta... utilice la funcion set_variables_lectura')
                    print('no se encontro la clave '+datos)
        if check:
            self.ultimo_lec=ultimo


########### Fin de definicion de la clase esp para las placas de control #######################

###################### Definicion de parametros de cada placa de control #######################

########################################### PLACA 1 ############################################
placa_1=esp()  # placa simple
# fuentes
placa_1.set_fuentes('Nivel_100_ACE')   
# topics
placa_1.set_topic_esc('FuentesHV/N_TIERRA/F_90kV/write')
placa_1.set_topic_lec('FuentesHV/N_TIERRA/F_90kV/read')    
# Fuente 090 kV
placa_1.set_variables_escritura({'Nivel_100_ACE_onoff':'encendidoF1','Nivel_100_ACE_setV':'setV_F1'})
placa_1.set_variables_lectura({'rdV_F1':'Nivel_100_ACE_getV','rdI_F1':'Nivel_100_ACE_getI'})
placa_1.activar()
######################################### FIN PLACA 1 ##########################################

########################################### PLACA 2 ############################################
placa_2=esp() # placa simple ############## ya funciona
# fuentes
placa_2.set_fuentes('Nivel_100_CUP')

# topics
placa_2.set_topic_esc('FuentesHV/N_100kV/F_100kV/write')
placa_2.set_topic_lec('FuentesHV/N_100kV/F_100kV/read')    
# Fuente 100 kV
placa_2.set_variables_escritura({'Nivel_100_CUP_onoff':'encendidoF1','Nivel_100_CUP_setV':'setV_F1'})
placa_2.set_variables_lectura({'rdV_F1':'Nivel_100_CUP_getV','rdI_F1':'Nivel_100_CUP_getI'})
placa_2.activar()
######################################### FIN PLACA 2 ##########################################

########################################### PLACA 3 ############################################
placa_3=esp() # placa doble ############### ya funciona
# fuentes
placa_3.set_fuentes('Nivel_200_CDO')
placa_3.set_fuentes('Nivel_200_ACE')   
# topics
placa_3.set_topic_esc('FuentesHV/N_110kV/F_110_190kV/write')
placa_3.set_topic_lec('FuentesHV/N_110kV/F_110_190kV/read')    
# Fuente 110 kV
placa_3.set_variables_escritura({'Nivel_200_CDO_onoff':'encendidoF1','Nivel_200_CDO_setV':'setV_F1'})
placa_3.set_variables_lectura({'rdV_F1':'Nivel_200_CDO_getV','rdI_F1':'Nivel_200_CDO_getI'})
# Fuente 190 kV
placa_3.set_variables_escritura({'Nivel_200_ACE_onoff':'encendidoF2','Nivel_200_ACE_setV':'setV_F2'})
placa_3.set_variables_lectura({'rdV_F2':'Nivel_200_ACE_getV','rdI_F2':'Nivel_200_ACE_getI'})
placa_3.activar()
######################################### FIN PLACA 3 ##########################################

########################################### PLACA 4 ############################################
placa_4=esp() # placa simple
# fuentes
placa_4.set_fuentes('Nivel_200_CUP')
# topics
placa_4.set_topic_esc('FuentesHV/N_200kV/F_200kV/write')
placa_4.set_topic_lec('FuentesHV/N_200kV/F_200kV/read')    
# Fuente 200 kV
placa_4.set_variables_escritura({'Nivel_200_CUP_onoff':'encendidoF1','Nivel_200_CUP_setV':'setV_F1'})
placa_4.set_variables_lectura({'rdV_F1':'Nivel_200_CUP_getV','rdI_F1':'Nivel_200_CUP_getI'})
placa_4.activar()
######################################### FIN PLACA 4 ##########################################

########################################### PLACA 5 ############################################
placa_5=esp() # placa triple
# fuentes
placa_5.set_fuentes('Nivel_300_CDO')
placa_5.set_fuentes('Nivel_300_ACE')
placa_5.set_fuentes('Nivel_300_CUP')
# topics
placa_5.set_topic_esc('FuentesHV/N_200kV/F_300kV/write')
placa_5.set_topic_lec('FuentesHV/N_200kV/F_300kV/read') 
# General
placa_5.set_variables_escritura({'Nivel_300_CDO_onoff':'encendido','Nivel_300_ACE_onoff':'encendido','Nivel_300_CUP_onoff':'encendido'})
placa_5.set_variables_lectura({'rdI_total':'Nivel_300_getI'})
# Fuente 210 kV
placa_5.set_variables_escritura({'Nivel_300_CDO_setV':'setV_f10k'})
placa_5.set_variables_lectura({'rdV_f10k':'Nivel_300_CDO_getV'})
# Fuente 290 kV
placa_5.set_variables_escritura({'Nivel_300_ACE_setV':'setV_f100k'})
placa_5.set_variables_lectura({'rdV_f100k':'Nivel_300_ACE_getV'})
# Fuente 300 kV
placa_5.set_variables_escritura({'Nivel_300_CUP_setV':'setV_f110k'})
placa_5.set_variables_lectura({'rdV_f110k':'Nivel_300_CUP_getV'})
placa_5.activar()
######################################### FIN PLACA 5 ##########################################

########################################### PLACA 6 ############################################
######################################### FIN PLACA 6 ##########################################

########################################### PLACA 7 ############################################
######################################### FIN PLACA 7 ##########################################

########################################### PLACA 8 ############################################
######################################### FIN PLACA 8 ##########################################

########################################### PLACA 9 ############################################
placa_9=esp() # placa supresora
# fuentes
placa_9.set_fuentes('Nivel_SUP')
placa_9.set_fuentes('Nivel_FAR')
# topics
placa_9.set_topic_esc('FuentesHV/N_Final/F_FaradayCup/write')
placa_9.set_topic_lec('FuentesHV/N_Final/F_FaradayCup/read')    
# Fuente Supresora
placa_9.set_variables_escritura({'Nivel_SUP_onoff':'encendido','Nivel_SUP_setV':'setV_supresora'})
placa_9.set_variables_lectura({'rdV_supresora':'Nivel_SUP_getV','rdI_supresora':'Nivel_SUP_getI'})
# Faraday
placa_9.set_variables_escritura({})
placa_9.set_variables_lectura({'corriente_blanco':'Nivel_FAR_getI'})
placa_9.activar()
######################################### FIN PLACA 9 ##########################################



##################EN PLACAS VAN LAS INSTANCIAS CREADAS QUE SE QUIERAN UTILIZAR #################

placas=[placa_1,placa_2,placa_3,placa_4,placa_5,placa_9]
global tiempo_sms
tiempo_sms=datetime.datetime.now()
dt=datetime.timedelta(seconds=0.2)
    
    
################################ CONFIGURACION BASE DE DATOS ####################################
# conectarse a la base de datos
import sqlite3

import os

conn = sqlite3.connect('./base_de_datos_acelerador.db')
curr = conn.cursor()

def insertar(que,donde): # funncion para insertar valores facilmente en la base de datos
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
        for param_lec in placa.lista_lec:
            s=s+placa.lista_lec[param_lec]+' text,'
    s=s[:-1]+')'
    print(s)
    curr.execute('CREATE TABLE escrituras '+s)

conn.commit()
conn.close()
############################# FIN CONFIGURACION BASE DE DATOS ####################################

#### esta funcion es llamada por el on_message del mqtt para guardar los datos #######
def escritura_db(): # escribe en la base de datos cuando recibo algun mensaje de una placa
    dic_vals={'tiempo':str(datetime.datetime.now().isoformat())}
    sdic_vals={}
    for placa in placas: # leo los ultimos valores de las placas y creo un diccionario
        dic_vals.update(placa.ultimo_lec)   
    for j in dic_vals: #convierto los valores a string
        sdic_vals.update({j:str(dic_vals[j])})
    insertar(sdic_vals,'escrituras') # inserto los valores en la base de datos
######################################################################################
    
###################### escrutura clasica del websocket ###############################
import asyncio
import websockets
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
t=threading.Thread(target=mqttc.loop_forever)
t.daemon = True
t.start()   
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