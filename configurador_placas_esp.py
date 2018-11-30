import threading
import sys
import time
import tkinter.ttk as ttk
import tkinter as tk
from tkinter import filedialog
import json

try:
    import paho.mqtt.client as mqtt
except ImportError:
    import os
    import inspect
    cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"../src")))
    if cmd_subfolder not in sys.path:
        sys.path.insert(0, cmd_subfolder)
    import paho.mqtt.client as mqtt


def on_connect(mqttc, obj, flags, rc):
    print("conectado al broker")

def on_message(mqttc, obj, msg):
    print(msg.topic+": "+str(msg.payload))

def on_publish(mqttc, obj, mid):
    print("mid: "+str(mid))

def on_subscribe(mqttc, obj, mid, granted_qos):
    print("Subscribed: "+str(mid)+" "+str(granted_qos))

def on_log(mqttc, obj, level, string):
    print(string)

server = "192.168.1.100"
mqttc = mqtt.Client()
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_publish = on_publish
mqttc.on_subscribe = on_subscribe
mqttc.connect(server, 1883, 60)

t=threading.Thread(target=mqttc.loop_forever)
t.daemon = True
t.start()   


def abrir_archivo_json():
    def enviar_configuracion():
        configurar_esp='ESP/'+dic_config['mac']+'/configurar'
        suscripcion=dic_config['rubro']+'/'+dic_config['nivel']+'/'+dic_config['fisico']+'/read'
        print('Se publica la configuracion en el topic: '+configurar_esp)
        print('Se suscribe al topic para escuchar el estado: '+suscripcion)
        mqttc.publish(configurar_esp, configuracion)
        mqttc.subscribe("FuentesHV/N_Final/F_FaradayCup/read" , 0)        
    
    archivo=tk.filedialog.askopenfilename(initialdir = "./",title = "Seleccione un archivo de configuracion",
                                       filetypes = (("Archivos JSON","*.json"),("all files","*.*")))    
    configuracion=open(archivo,"r").read()
    dic_config=json.loads(configuracion)
    list_param=dic_config.pop('param',None)
    for widget in frame_ver_json.winfo_children():
        widget.destroy()
    note=ttk.Notebook(frame_ver_json)
    nombres=[]
    datos=[]
    nombres_param=[]
    datos_param=[]
    nombre_frame=['General']
    f=[ttk.Frame(note)]
    for h in range(len(list_param)):
        f.append(ttk.Frame(note))
        nombre_frame.append(list_param[h]['desc'])
    for s in range(len(f)):
        note.add(f[s],text=nombre_frame[s])
        
    for etiqueta in dic_config:        
        nombres.append(ttk.Label(f[0],text=etiqueta))
        datos.append(ttk.Label(f[0],text=str(dic_config[etiqueta]),wraplength="300"))
    for n_par,par in enumerate(list_param):    
        for p in par:        
            nombres.append(ttk.Label(f[n_par+1],text=p))
            datos.append(ttk.Label(f[n_par+1],text=str(par[p]),wraplength="300"))
    for j in range(len(nombres)):
        nombres[j].grid(column=0,row=j+1)
        datos[j].grid(column=1,row=j+1)
    
    note.grid(column=0,columnspan=2,row=1)   
    boton_enviar=ttk.Button(principal,text='Enviar archivo',command=enviar_configuracion)
    boton_enviar.grid(column=0,row=2)
    
        
principal=tk.Tk()
principal.geometry('600x500')
boton_abrir=ttk.Button(principal,text='Abrir archivo',command=abrir_archivo_json)
frame_ver_json=ttk.Frame(principal)
boton_abrir.grid(column=0,row=0)
frame_ver_json.grid(column=0,row=1)
principal.mainloop()
