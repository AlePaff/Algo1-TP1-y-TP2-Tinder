from datos_prueba import diccionarioPrueba

nuevo = open("nuevaBase.csv","w")

claves=diccionarioPrueba.keys()

for pseudonimos in claves:
	nombre,apellido,contraseña,sexo,edad,ubicacion, intereses, likes,mensajes = diccionarioPrueba[pseudonimos].values()
	
	latitud,longitud=ubicacion

	guardar = "{0};{1};{2};{3};{4};{5};{6};{7};{8};{9};{10}\n".format(pseudonimos, nombre,apellido,contraseña,sexo,edad,latitud,longitud, ",".join(intereses), likes, mensajes)
	
	nuevo.write(guardar)

	
nuevo.close()