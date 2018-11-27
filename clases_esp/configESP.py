from .espClass import esp

### Definimos las placas a controlar usando la clase esp (ver espClass.py)
########################################### PLACA 1 ###########################
placa_1 = esp()  # placa simple
# fuentes
placa_1.set_fuentes('Nivel_100_ACE')
# topics
placa_1.set_topic_esc('FuentesHV/N_TIERRA/F_90kV/write')
placa_1.set_topic_lec('FuentesHV/N_TIERRA/F_90kV/read')
# Fuente 090 kV
placa_1.set_variables_escritura({'Nivel_100_ACE_onoff':'encendidoF1',
                                 'Nivel_100_ACE_setV':'setV_F1'})
placa_1.set_variables_lectura({'rdV_F1':'Nivel_100_ACE_getV',
                               'rdI_F1':'Nivel_100_ACE_getI'})
placa_1.activar()
######################################### FIN PLACA 1 #########################

########################################### PLACA 2 ###########################
placa_2 = esp() # placa simple ############## ya funciona
# fuentes
placa_2.set_fuentes('Nivel_100_CUP')

# topics
placa_2.set_topic_esc('FuentesHV/N_100kV/F_100kV/write')
placa_2.set_topic_lec('FuentesHV/N_100kV/F_100kV/read')
# Fuente 100 kV
placa_2.set_variables_escritura({'Nivel_100_CUP_onoff':'encendidoF1',
                                 'Nivel_100_CUP_setV':'setV_F1'})
placa_2.set_variables_lectura({'rdV_F1':'Nivel_100_CUP_getV',
                               'rdI_F1':'Nivel_100_CUP_getI'})
placa_2.activar()
######################################### FIN PLACA 2 #########################

########################################### PLACA 3 ###########################
placa_3 = esp() # placa doble ############### ya funciona
# fuentes
placa_3.set_fuentes('Nivel_200_CDO')
placa_3.set_fuentes('Nivel_200_ACE')
# topics
placa_3.set_topic_esc('FuentesHV/N_110kV/F_110_190kV/write')
placa_3.set_topic_lec('FuentesHV/N_110kV/F_110_190kV/read')
# Fuente 110 kV
placa_3.set_variables_escritura({'Nivel_200_CDO_onoff': 'encendidoF1',
                                 'Nivel_200_CDO_setV': 'setV_F1'})
placa_3.set_variables_lectura({'rdV_F1': 'Nivel_200_CDO_getV',
                               'rdI_F1': 'Nivel_200_CDO_getI'})
# Fuente 190 kV
placa_3.set_variables_escritura({'Nivel_200_ACE_onoff': 'encendidoF2',
                                 'Nivel_200_ACE_setV': 'setV_F2'})
placa_3.set_variables_lectura({'rdV_F2': 'Nivel_200_ACE_getV',
                               'rdI_F2': 'Nivel_200_ACE_getI'})
placa_3.activar()
######################################### FIN PLACA 3 ########################

########################################### PLACA 4 ###########################
placa_4 = esp() # placa simple
# fuentes
placa_4.set_fuentes('Nivel_200_CUP')
# topics
placa_4.set_topic_esc('FuentesHV/N_200kV/F_200kV/write')
placa_4.set_topic_lec('FuentesHV/N_200kV/F_200kV/read')
# Fuente 200 kV
placa_4.set_variables_escritura({'Nivel_200_CUP_onoff': 'encendidoF1',
                                 'Nivel_200_CUP_setV': 'setV_F1'})
placa_4.set_variables_lectura({'rdV_F1': 'Nivel_200_CUP_getV',
                               'rdI_F1': 'Nivel_200_CUP_getI'})
placa_4.activar()
######################################### FIN PLACA 4 #########################

########################################### PLACA 5 ###########################
placa_5 = esp()  # placa triple
# fuentes
placa_5.set_fuentes('Nivel_300_CDO')
placa_5.set_fuentes('Nivel_300_ACE')
placa_5.set_fuentes('Nivel_300_CUP')
# topics
placa_5.set_topic_esc('FuentesHV/N_200kV/F_300kV/write')
placa_5.set_topic_lec('FuentesHV/N_200kV/F_300kV/read')
# General
placa_5.set_variables_escritura({'Nivel_300_CDO_onoff': 'encendido',
                                 'Nivel_300_ACE_onoff': 'encendido',
                                 'Nivel_300_CUP_onoff': 'encendido'})
placa_5.set_variables_lectura({'rdI_total': 'Nivel_300_getI'})
# Fuente 210 kV
placa_5.set_variables_escritura({'Nivel_300_CDO_setV': 'setV_f10k'})
placa_5.set_variables_lectura({'rdV_f10k': 'Nivel_300_CDO_getV'})
# Fuente 290 kV
placa_5.set_variables_escritura({'Nivel_300_ACE_setV': 'setV_f100k'})
placa_5.set_variables_lectura({'rdV_f100k': 'Nivel_300_ACE_getV'})
# Fuente 300 kV
placa_5.set_variables_escritura({'Nivel_300_CUP_setV': 'setV_f110k'})
placa_5.set_variables_lectura({'rdV_f110k': 'Nivel_300_CUP_getV'})
placa_5.activar()
######################################### FIN PLACA 5 #########################

########################################### PLACA 6 ###########################
######################################### FIN PLACA 6 #########################

########################################### PLACA 7 ###########################
######################################### FIN PLACA 7 #########################

########################################### PLACA 8 ###########################
######################################### FIN PLACA 8 #########################

########################################### PLACA 9 ###########################
placa_9 = esp()  # placa supresora
# fuentes
placa_9.set_fuentes('Nivel_SUP')
placa_9.set_fuentes('Nivel_FAR')
# topics
placa_9.set_topic_esc('FuentesHV/N_Final/F_FaradayCup/write')
placa_9.set_topic_lec('FuentesHV/N_Final/F_FaradayCup/read')
# Fuente Supresora
placa_9.set_variables_escritura({'Nivel_SUP_onoff': 'encendido',
                                 'Nivel_SUP_setV': 'setV_supresora'})
placa_9.set_variables_lectura({'rdV_supresora': 'Nivel_SUP_getV',
                               'rdI_supresora': 'Nivel_SUP_getI'})
# Faraday
placa_9.set_variables_escritura({})
placa_9.set_variables_lectura({'corriente_blanco': 'Nivel_FAR_getI'})
placa_9.activar()
######################################### FIN PLACA 9 #########################