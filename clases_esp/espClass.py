import json
import datetime


class esp():
    '''
    Clase que representa las placas de control, ya sea con una o dos fuentes a
    controlar. Las placas tienen disponibles 4 lecturas analogicas de 0 a 10V,
    2 escrituras analogicas (DAC) de 0 a 10V y 2 reles.
    Las lecturas se utilizan para leer el estado de las fuentes, 
    tension y corriente. Las escrituras se usan para setear el valor
    de tension de las fuentes.
    Los reles son para habilitar la salida de alta tension de cada fuente.
    '''
    def __init__(self):
        '''
        Inicializa la clase con la cantidad de valores necesarios
        para las fuentes conectadas a esta placa.
        Asi como el template de los mensajes a enviar y los topics
        necesarios para comunicarse mediante MQTT.
        lista_lec: Diccionario con las variables a leer de la/s fuente/s.
        lista_esc: Diccionario con las variables a escribir en la/s fuente/s.
        lista_fuentes: Set con las fuentes controladas por la placa.
        ultimo_lec: Diccionario con las ultimas lecturas
        ultimo_esc: Diccionario con los ultimos valores leidos
        ultimo_tiempo: Hora de ultima comunicacion de la esp
        '''
        self.variables_lectura = {}
        self.variables_escritura = {}
        self.lista_fuentes = set()
        self.ultimo_lec = {}
        self.ultimo_esc = {}
        self.ultimo_dif = {}
        self.ultimo_tiempo = datetime.datetime.now()
        
    def activar(self):
        '''
        Inicializa en 0 todos los valores de escritura de la placa.
        Inicializa en 0 todos los valores de lectura de la placa.
        '''
        for key in self.variables_escritura:
            self.ultimo_esc[key] = 0

        for key in self.variables_lectura:
            self.ultimo_lec[key] = 0            

    def set_fuentes(self, lista: str):
        '''
        Asignar nombres locales (a nivel soft de control) de las
        fuentes que controla la placa.
        lista: String con nombre de la fuente a agregar.
        '''
        self.lista_fuentes.add(lista)
        
    def set_variables_lectura(self, lista_variables: dict):
        '''
        Mapea los nombres locales para la lectura, a los nombres del firmware
        de la placa.
        lista_variables: Diccionario con el mapeo
        i.e. Nombre local: "Nivel_200_CDO_getV" -> Nombre firmware: "rdV_F1"
        {'Nivel_200_CUP_onoff':'encendidoF1','Nivel_200_CUP_setV':'setV_F1'}
        '''
        self.variables_lectura.update(lista_variables)
    
            
    def set_variables_escritura(self, lista_variables: dict):
        '''
        Mapea los nombres locales para la escritura, a los nombres del firmware
        de la placa.
        lista_variables: Diccionario con el mapeo
        i.e. Nombre local: "Nivel_200_CDO_setV" -> Nombre firmware: "setV_F1"
        {'Nivel_600_ACE_getV': {'mas':'rdV_f100k','menos':'rdV_f10k'}}
        {'Nivel_200_CDO_getV':'rdV_F1','Nivel_200_CDO_getI':'rdI_F1'}
        '''
        self.variables_escritura.update(lista_variables)
        
    def set_topic_esc(self, topic: str):
        '''
        Asigna el topic de MQTT para escritura de la placa.
        topic: String con el topic
        i.e. "FuentesHV/N_110kV/F_110_190kV/write"
        '''
        self.topic_esc = topic
        
    def set_topic_lec(self, topic: str):
        '''
        Asigna el topic de MQTT para lectura de la placa.
        topic: String con el topic
        i.e. "FuentesHV/N_110kV/F_110_190kV/read"
        '''
        self.topic_lec = topic

    def set_valores(self, valores: dict):
        '''
        Crea un mensaje para mandar al broker MQTT con los valores para
        setear en la/s fuente/s.
        valores: Diccionario con los valores de seteo de la/s fuente/s
        '''
        mensaje = {}
        if len(valores) != len(self.variables_escritura):
            print('la cantidad de valores a setear es incorrecta')
            print('se esperan', len(self.variables_escritura), 'valores')
            print('se recibieron', len(valores), 'valores')
        else:
            for datos in valores:
                if datos in self.variables_escritura.keys():
                    mensaje[self.variables_escritura[datos]] = valores[datos]
                    mensaje_completo = (self.topic_esc, str(mensaje))
                else:
                    print('lista de escritura incorrecta... \
                          utilice la funcion set_variables_escritura')
                    print('no se encontro la clave ' + datos)
                    print(datos, valores[datos], 'no asignado')
            return mensaje_completo

    def get_valores(self, msg):
        '''
        Lee un mensaje que le manda el broker MQTT y guarda los datos dentro de
        la instancia con los nombres locales.
        valores: Diccionario con los valores de seteo de la/s fuente/s
        '''
        check = True
        mensaje = json.loads(msg.payload)

        ultimo={key:0 for key in self.variables_lectura.keys()}
        for nombres_locales in self.variables_lectura.keys():
            if isinstance(self.variables_lectura[nombres_locales],dict): #si la asignacion es por diccionario
                try: # intento leer la clave mas
                    if 'mas' in self.variables_lectura[nombres_locales].keys():
                        ultimo[nombres_locales]+=mensaje[self.variables_lectura[nombres_locales]['mas']]
                except:
                    print('las claves en "mas" son incorrectas')
                    print("'"+self.variables_lectura[nombres_locales]['mas']+"'")
                    print(mensaje.keys())
                    check=False
                try: # intento leer la clave menos
                    if 'menos' in self.variables_lectura[nombres_locales].keys():
                        ultimo[nombres_locales]-=mensaje[self.variables_lectura[nombres_locales]['menos']]
                except:
                    print('las claves en "menos" son incorrectas')
                    print("'"+self.variables_lectura[nombres_locales]['menos']+"'")
                    print(mensaje.keys())
                    check=False
            else: #si la asignacion es directa
                try:
                    ultimo[nombres_locales]=mensaje[self.variables_lectura[nombres_locales]]
                except:
                    check=False
        if check==False: # si hay algun error escribo Error_Lec en todas las claves
            ultimo={key:'Error_Lec' for key in self.variables_lectura.keys()}
        self.ultimo_lec=ultimo # actualizo la lectura
