import json
import datetime

class esp():
    '''
    Clase que representa las placas de cnntrol, ya sea con una o dos fuentes a controlar. 
    Las placas tienen disponibles 4 lecturas analogicas de 0 a 10V, 2 escrituras analogicas (DAC)
    de 0 a 10V y 2 reles.
    Las lecturas se utilizan para leer el estado de las fuentes, tension y corriente.
    Las escrituras se usan para setear el valor de tension de las fuentes.
    Los reles son para habilitar la salida de alta tension de cada fuente.
    '''
    def __init__(self):
        '''
        Inicializa la clase con la cantidad de valores necesarios para las fuentes conectadas a esta placa.
        Asi como el template de los mensajes a enviar y los topics necesarios para comunicarse mediante MQTT
        '''
        self.lista_lec={}
        self.lista_esc={}
        self.lista_fuentes=set()
        self.ultimo_esc={}
        self.ultimo_lec={}
        self.ultimo_tiempo=datetime.datetime.now()
        
    def activar(self):
        '''
        Asignar 0 a todos los valores de escritura de la placa.
        '''
        for s in self.lista_esc:
            self.ultimo_esc[s]=0
             
    def set_fuentes(self, lista):
        '''
        Asignar nombres externos de las fuentes que controla la placa.
        '''
        self.lista_fuentes.add(lista)
        
    def set_variables_lectura(self, lista_variables):
        '''
        asignar nombres externos a las variables que lee la placa.
        '''
        self.lista_lec.update(lista_variables)
        for j in lista_variables:
            self.ultimo_lec.update({lista_variables[j]:0})
            
    def set_variables_escritura(self, lista_variables):
        '''
        Asignar nombres externos a las variables que escribe la placa.
        '''
        self.lista_esc.update(lista_variables)
        
    def set_topic_esc(self, topic):
        '''
        Asignar el topic de escritura de la placa.
        '''
        self.topic_esc=topic
        
    def set_topic_lec(self, topic):
        '''
        Asignar el topic de lectura de la placa.
        '''
        self.topic_lec=topic    
        
    def set_valores(self, valores):
        '''
        Crea un mensaje para mandar al broker.
        '''
        mensaje = {}
        if len(valores)!=len(self.lista_esc):
            print('la cantidad de valores a setear es incorrecta')
            print('se esperan', len(self.lista_esc), 'valores')
            print('se recibieron', len(valores), 'valores')
        else:
            for datos in valores:
                if datos in self.lista_esc.keys():
                    mensaje[self.lista_esc[datos]] = valores[datos]
                    mensaje_completo=(self.topic_esc, str(mensaje))
                else:
                    print('lista de escritura incorrecta... utilice la funcion set_variables_escritura')
                    print('no se encontro la clave '+datos)
                    print(datos, valores[datos], 'no asignado')
            return mensaje_completo
    
    def get_valores(self, msg):
        '''
        Lee un mensaje que le manda el broker y guarda los datos dentro de la instancia con los nombres externos.
        '''
        check = True
        ultimo = {}
        mensaje = json.loads(msg.payload)
        if len(mensaje) != len(self.lista_lec):
            check = False
            print('la cantidad de valores leidos es incorrecta')
            print('se esperan', len(self.lista_lec), 'valores')
            print('se recibieron', len(mensaje), 'valores')            
        else:
            for datos in mensaje:
                if datos in self.lista_lec.keys():
                    ultimo[self.lista_lec[datos]] = mensaje[datos]
                else:
                    check = False
                    print('lista de lectura incorrecta... utilice la funcion set_variables_lectura')
                    print('no se encontro la clave '+datos)
        if check:
            self.ultimo_lec = ultimo