import json


a={'rdV_f10k': 5.02,'rdV_f100k': 20.00,'rdV_f110k': 22.00,'rdI_total':1.345}
p={'Nivel_300_CDO_getV':a['rdV_f10k'],'Nivel_300_ACE_setV':a['rdV_f100k']-a['rdV_f10k'],'Nivel_300_CUP_setV':a['rdV_f110k']-a['rdV_f100k']}


variables_lectura_2={'rdV_f10k': 'Nivel_300_CDO_getV', 'rdI_total': 'Nivel_300_getI','rdV_f100k': 'Nivel_300_ACE_getV', 'rdV_f110k': 'Nivel_300_CUP_getV'}
variables_lectura={'Nivel_300_ACE_getV':{'mas':'rdV_f100k','menos':'rdV_f10k'},
'Nivel_300_CDO_getV':{'mas':'rdV_f10k'},

'Nivel_300_CUP_getV':{'mas':'rdV_f110k','menos':'rdV_f100k'},
'Nivel_300_getI':{'mas':'rdI_total'}}

check = True
ultimo = {}
mensaje = a

r={h1:0 for h1 in variables_lectura.keys()}

for nombres_dan in variables_lectura.keys():
	if isinstance(variables_lectura[nombres_dan],dict):
		try:
			if 'mas' in variables_lectura[nombres_dan].keys():
				r[nombres_dan]+=a[variables_lectura[nombres_dan]['mas']]
		except:
			print('las claves en "mas" son incorrectas')
			print("'"+variables_lectura[nombres_dan]['mas']+"'")
			print(a.keys())
			check=False
		try:
			if 'menos' in variables_lectura[nombres_dan].keys():
				r[nombres_dan]-=a[variables_lectura[nombres_dan]['menos']]
		except:
			print('las claves en "menos" son incorrectas')
			print("'"+variables_lectura[nombres_dan]['menos']+"'")
			print(a.keys())
			check=False
	else:
	 	try:
	 		r[nombres_dan]=a[variables_lectura[nombres_dan]]
	 	except:
	 		check=False
if check==False:
	r={h1:'Error_Lec' for h1 in variables_lectura.keys()}
print(r)

