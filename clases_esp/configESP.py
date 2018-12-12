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
placa_1.set_variables_escritura({'Nivel_100_ACE_setO':'encendidoF1',
                                 'Nivel_100_ACE_setV':'setV_F1'})
placa_1.set_variables_lectura({'Nivel_100_ACE_getV':'rdV_F1',
                               'Nivel_100_ACE_getI':'rdI_F1'})
placa_1.activar()
######################################### FIN PLACA 1 #########################

########################################### PLACA 2 ###########################
placa_2 = esp() # placa simple
# fuentes
placa_2.set_fuentes('Nivel_100_CUP')

# topics
placa_2.set_topic_esc('FuentesHV/N_100kV/F_100kV/write')
placa_2.set_topic_lec('FuentesHV/N_100kV/F_100kV/read')
# Fuente 100 kV
placa_2.set_variables_escritura({'Nivel_100_CUP_setO':'encendidoF1',
                                 'Nivel_100_CUP_setV':'setV_F1'})
placa_2.set_variables_lectura({'Nivel_100_CUP_getV':'rdV_F1',
                               'Nivel_100_CUP_getI':'rdI_F1'})
placa_2.activar()
######################################### FIN PLACA 2 #########################

########################################### PLACA 3 ###########################
placa_3 = esp() # placa doble 
# fuentes
placa_3.set_fuentes('Nivel_200_CDO')
placa_3.set_fuentes('Nivel_200_ACE')
# topics
placa_3.set_topic_esc('FuentesHV/N_110kV/F_110_190kV/write')
placa_3.set_topic_lec('FuentesHV/N_110kV/F_110_190kV/read')
# Fuente 110 kV
placa_3.set_variables_escritura({'Nivel_200_CDO_setO':'encendidoF1',
                                 'Nivel_200_CDO_setV':'setV_F1'})
placa_3.set_variables_lectura({'Nivel_200_CDO_getV':'rdV_F1',
                               'Nivel_200_CDO_getI':'rdI_F1'})
# Fuente 190 kV
placa_3.set_variables_escritura({'Nivel_200_ACE_setO':'encendidoF2',
                                 'Nivel_200_ACE_setV':'setV_F2'})
placa_3.set_variables_lectura({'Nivel_200_ACE_getV':'rdV_F2',
                               'Nivel_200_ACE_getI':'rdI_F2'})
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
placa_4.set_variables_escritura({'Nivel_200_CUP_setO': 'encendidoF1',
                                 'Nivel_200_CUP_setV': 'setV_F1'})
placa_4.set_variables_lectura({'Nivel_200_CUP_getV':'rdV_F1',
                               'Nivel_200_CUP_getI':'rdI_F1'})
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
placa_5.set_variables_escritura({'Nivel_300_CDO_setO': 'encendido',
                                 'Nivel_300_ACE_setO': 'encendido',
                                 'Nivel_300_CUP_setO': 'encendido'})
placa_5.set_variables_lectura({'Nivel_300_getI':'rdI_total'})
# Fuente 210 kV
placa_5.set_variables_escritura({'Nivel_300_CDO_setV': 'setV_f10k'})
placa_5.set_variables_lectura({'Nivel_300_CDO_getV': 'rdV_f10k'})
# Fuente 290 kV
placa_5.set_variables_escritura({'Nivel_300_ACE_setV': 'setV_f100k'})
placa_5.set_variables_lectura({'Nivel_300_ACE_getV': {'mas':'rdV_f100k','menos':'rdV_f10k'}})
# Fuente 300 kV
placa_5.set_variables_escritura({'Nivel_300_CUP_setV': 'setV_f110k'})
placa_5.set_variables_lectura({'Nivel_300_CUP_getV': {'mas':'rdV_f110k','menos':'rdV_f100k'}})
placa_5.activar()
######################################### FIN PLACA 5 #########################

########################################### PLACA 6 ###########################
placa_6 = esp()  # placa triple
# fuentes
placa_6.set_fuentes('Nivel_400_CDO')
placa_6.set_fuentes('Nivel_400_ACE')
placa_6.set_fuentes('Nivel_400_CUP')
# topics
placa_6.set_topic_esc('FuentesHV/N_400kV/F_400kV/write')
placa_6.set_topic_lec('FuentesHV/N_400kV/F_400kV/read')
# General
placa_6.set_variables_escritura({'Nivel_400_CDO_setO': 'encendido',
                                 'Nivel_400_ACE_setO': 'encendido',
                                 'Nivel_400_CUP_setO': 'encendido'})
placa_6.set_variables_lectura({'Nivel_400_getI': 'rdI_total'})
# Fuente 310 kV
placa_6.set_variables_escritura({'Nivel_400_CDO_setV': 'setV_f110k'})
placa_6.set_variables_lectura({'Nivel_400_CDO_getV': {'mas':'rdV_f110k','menos':'rdV_f100k'}})
# Fuente 390 kV
placa_6.set_variables_escritura({'Nivel_400_ACE_setV': 'setV_f100k'})
placa_6.set_variables_lectura({'Nivel_400_ACE_getV': {'mas':'rdV_f100k','menos':'rdV_f10k'}})
# Fuente 400 kV
placa_6.set_variables_escritura({'Nivel_400_CUP_setV': 'setV_f10k'})
placa_6.set_variables_lectura({'Nivel_400_CUP_getV': 'rdV_f10k'})
placa_6.activar()
######################################### FIN PLACA 6 #########################

########################################### PLACA 7 ###########################
placa_7 = esp()  # placa triple
# fuentes
placa_7.set_fuentes('Nivel_500_CDO')
placa_7.set_fuentes('Nivel_500_ACE')
placa_7.set_fuentes('Nivel_500_CUP')
# topics
placa_7.set_topic_esc('FuentesHV/N_400kV/F_500kV/write')
placa_7.set_topic_lec('FuentesHV/N_400kV/F_500kV/read')
# General
placa_7.set_variables_escritura({'Nivel_500_CDO_setO': 'encendido',
                                 'Nivel_500_ACE_setO': 'encendido',
                                 'Nivel_500_CUP_setO': 'encendido'})
placa_7.set_variables_lectura({'Nivel_500_getI': 'rdI_total'})
# Fuente 410 kV
placa_7.set_variables_escritura({'Nivel_500_CDO_setV': 'setV_f10k'})
placa_7.set_variables_lectura({'Nivel_500_CDO_getV': 'rdV_f10k'})
# Fuente 490 kV
placa_7.set_variables_escritura({'Nivel_500_ACE_setV': 'setV_f100k'})
placa_7.set_variables_lectura({'Nivel_500_ACE_getV': {'mas':'rdV_f100k','menos':'rdV_f10k'}})
# Fuente 500 kV
placa_7.set_variables_escritura({'Nivel_500_CUP_setV': 'setV_f110k'})
placa_7.set_variables_lectura({'Nivel_500_CUP_getV': {'mas':'rdV_f110k','menos':'rdV_f100k'}})
placa_7.activar()
######################################### FIN PLACA 7 #########################

########################################### PLACA 8 ###########################
placa_8 = esp()  # placa triple
# fuentes
placa_8.set_fuentes('Nivel_600_CDO')
placa_8.set_fuentes('Nivel_600_ACE')
placa_8.set_fuentes('Nivel_600_CUP')
# topics
placa_8.set_topic_esc('FuentesHV/N_600kV/F_600kV/write')
placa_8.set_topic_lec('FuentesHV/N_600kV/F_600kV/read')
# General
placa_8.set_variables_escritura({'Nivel_600_CDO_setO': 'encendido',
                                 'Nivel_600_ACE_setO': 'encendido',
                                 'Nivel_600_CUP_setO': 'encendido'})
placa_8.set_variables_lectura({'Nivel_600_getI': 'rdI_total'})
# Fuente 510 kV
placa_8.set_variables_escritura({'Nivel_600_CDO_setV': 'setV_f110k'})
placa_8.set_variables_lectura({'Nivel_600_CDO_getV': {'mas':'rdV_f110k','menos':'rdV_f100k'}})
# Fuente 590 kV
placa_8.set_variables_escritura({'Nivel_600_ACE_setV': 'setV_f100k'})
placa_8.set_variables_lectura({'Nivel_600_ACE_getV': {'mas':'rdV_f100k','menos':'rdV_f10k'}})
# Fuente 600 kV
placa_8.set_variables_escritura({'Nivel_600_CUP_setV': 'setV_f10k'})
placa_8.set_variables_lectura({'Nivel_600_CUP_getV': 'rdV_f10k'})
placa_8.activar()
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
placa_9.set_variables_escritura({'Nivel_SUP_setO': 'encendido',
                                 'Nivel_SUP_setV': 'setV_supresora'})
placa_9.set_variables_lectura({'Nivel_SUP_getV': 'rdV_supresora',
                               'Nivel_SUP_getI': 'rdI_supresora'})
# Faraday
# placa_9.set_variables_escritura({})
placa_9.set_variables_lectura({'Nivel_FAR_getI': 'corriente_blanco'})
placa_9.activar()
######################################### FIN PLACA 9 #########################

########################################### PLACA 0 ###########################
placa_0 = esp() # placa simple
# fuentes
placa_0.set_fuentes('Nivel_030_ACE')
# topics
placa_0.set_topic_esc('FuentesHV/N_TIERRA/F_30kV/write')
placa_0.set_topic_lec('FuentesHV/N_TIERRA/F_30kV/read')
# Fuente -30 kV
placa_0.set_variables_escritura({'Nivel_030_ACE_setO': 'encendidoF1',
                                 'Nivel_030_ACE_setV': 'setV_F1'})
placa_0.set_variables_lectura({'Nivel_030_ACE_getV': 'rdV_F1',
                               'Nivel_030_ACE_getI': 'rdI_F1'})
placa_0.activar()
######################################### FIN PLACA 0 #########################