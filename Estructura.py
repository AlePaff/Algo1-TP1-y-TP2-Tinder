from math import floor
from geopy.distance import vincenty	 # instalar geopy, ejecutar desde la consola   tambien funciona con "great_circle"
from pickle import dump, load



#----------------------BLOQUE MENU------------------------
def menuPrincipal():
	opcionesMenuPrincipal = ""	#inicializa la variable
	print("""
  _____   _               _               
 |_   _| (_)  _ __     __| |   ___   _ __ 
   | |   | | | '_ \   / _` |  / _ \ | '__|
   | |   | | | | | | | (_| | |  __/ | |   
   |_|   |_| |_| |_|  \__,_|  \___| |_|   """)
	while opcionesMenuPrincipal!="5":
		opcionesMenuPrincipal = input ("""
(1) IMPRIMIR USUARIOS REGISTRADOS
(2) CREAR CUENTA NUEVA
(3) INGRESAR AL SISTEMA
(4) IMPRIMIR TOP5 USUARIOS
(5) CERRAR PROGRAMA
Escriba el numero de opcion deseada: 
""")

		if opcionesMenuPrincipal == "1":
			nuevosUsuarios00=open(r"nuevosUsuarios.pkl","rb")
			usuariosPredefinidos00=open(r"usuariosPredefinidos.csv","r")
			imprimirUsuarios(usuariosPredefinidos00,nuevosUsuarios00)
			nuevosUsuarios00.close()
			usuariosPredefinidos00.close()
		elif opcionesMenuPrincipal == "2":
			crearUsuario () # llama una func, la cual sirve para cargar datos, y esto aladirlos al diccionario principal, osea a "datos"
		elif opcionesMenuPrincipal == "3":
			ingresarSistema ()
		elif opcionesMenuPrincipal=="4":
			cantLikes,nombres=top5()	#desempaqueta las dos tuplas, en dos lista independientes
			print("Los usuarios con más likes son...")
			for usuario in zip(cantLikes,nombres):
				print(usuario[1],"con",usuario[0],"likes")
		elif opcionesMenuPrincipal=="5":
			return
		else:
			print ("Por favor, ingrese una de las opciones")


def ingresarSistema():
	ejecucionActual["pseu"] = str (input ("Ingrese su nombre de usuario:"))
	if ejecucionActual["pseu"] in ejecucionActual["listaUsers"]:
		contraseña = input ("Ingrese su contraseña: ")
		if contraseña == datos[ejecucionActual["pseu"]]["contraseña"]:
			print ("Hola", datos[ejecucionActual["pseu"]]["nombre"])
			menuSecundario ()
		else:
			print ("Contraseña incorrecta")
	else:
		print ("Usuario inválido, volviendo al menu principal")


def menuSecundario():
	opcionesMenuSecundario = input ("""
(1) BUSCAR GENTE
(2) MENSAJES
(3) EDITAR
(4) SALIR DEL SISTEMA	
""")
	while opcionesMenuSecundario!="4":
		if opcionesMenuSecundario == "1":
			a,b,c=filtrarBusquedas()	#la funcion filtrarBusquedas, devuelve 3 variables
			hacerBusqueda(a,b,c)	#hacerBusqueda necesita 3 parametros
			
		elif opcionesMenuSecundario == "2":
			interfazMensajes()
		elif opcionesMenuSecundario == "3":
			print ("Funcion aun sin terminar")
		elif opcionesMenuSecundario == "4":
			print ("Adios, gracias por visitar Tinder")
			return
		else:
			print ("Por favor, ingrese una de las opciones")
		opcionesMenuSecundario = input ("""
(1) BUSCAR GENTE
(2) MENSAJES
(3) EDITAR
(4) SALIR DEL SISTEMA	
""")
			
			



	

	
#--------------BLOQUE BUSQUEDA-------------------
def filtrarBusquedas():
	ubicacionUsuarioLogueado = datos[ejecucionActual["pseu"]]["ubicacion"]		  
	sexoInt = definirSexoInt()
	edadMinima = int (input ("Ingrese la edad mínima del rango de búsqueda:"))
	edadMaxima = int (input ("Ingrese la edad máxima del rango de búsqueda:"))
	
	#entra en este while si, el usuario no ingresa en un rango de edades valido, o si la edad minima es mayor o igual que la maxima
	while (not (validarEdad(edadMaxima)) or (not validarEdad (edadMinima))) or (edadMinima>=edadMaxima):
		print ("Por favor ingrese un rango de edad de entre 18 y 99 años.")
		edadMinima = int(input("Ingrese una edad minima (mayor o igual a 18):"))
		edadMaxima = int(input("Ingrese una edad maxima (menor o igual a 99):"))

	radioDeBusq = int(input("Ingrese un radio de busqueda en km: "))
	
	return sexoInt, [edadMinima, edadMaxima], radioDeBusq

	
	
	
	
def hacerBusqueda(sexoDeInteres, rangoEdades, radioBusqueda):
	copiaListaUsers=ejecucionActual["listaUsers"][:]	#crea una copia, para actualizarla a la original mas tarde
	
	if ejecucionActual["pseu"] in ejecucionActual["listaUsers"]:	#el if, es por si hizo una segunda busqueda
		ejecucionActual["listaUsers"].remove(ejecucionActual["pseu"])  # elimina de la lista de usuarios, el usuario logueado (para que no aparezca él mismo en la busqueda)
		
	ubicacionUsuarioLogueado = datos[ejecucionActual["pseu"]]["ubicacion"]
	interesesUsuarioLogueado = datos[ejecucionActual["pseu"]]["intereses"]
	
	# recorre la longitud de la lista de usuarios
	for numUser in range (len(ejecucionActual["listaUsers"])):
		usuarioElegido=ejecucionActual["listaUsers"][numUser]	#es un string, en este caso, un pseudonimo
		if hacerBusquedaModularizado(usuarioElegido,ubicacionUsuarioLogueado,interesesUsuarioLogueado,sexoDeInteres, rangoEdades, radioBusqueda)=="S":
			ejecucionActual["listaUsers"]=copiaListaUsers
			return
	return print ("La busqueda ha finalizado.")
	
	
	

def hacerBusquedaModularizado(usuarioElegido,ubicacionUsuarioLogueado,interesesUsuarioLogueado,sexoDeInteres, rangoEdades, radioBusqueda):
	# va a repetirse las veces como numero de usuario haya y va a recorrer la lista de usuarios
	# las variables de aca abajo cambian en cada iteracion

	sexo = datos[usuarioElegido]["sexo"]	 
	ubicacion = datos[usuarioElegido]["ubicacion"]
	edad = datos[usuarioElegido]["edad"]
	intereses = datos[usuarioElegido]["intereses"]
	
	# para el caso que busco H y M, osea si hay dos elementos en la lista "sexoDeInteres"
	if ((len (sexoDeInteres)) == 2 or (sexo == "I")):
		if (rangoEdades[0] <= edad and rangoEdades[1] >= edad) and ((distanciaEntreDos (ubicacionUsuarioLogueado, ubicacion)) <= radioBusqueda):
			porcentajeCoin = calcularPorcentaje (interesesUsuarioLogueado, intereses)
			print ("-"*40,"\n",usuarioElegido, "y tu tienen {}% de coincidencia".format (porcentajeCoin))
	
			#llama a la funcion opcionesBusqueda
			if (opcionesBusqueda (usuarioElegido))=="S":	# si puso salir, vuelve al menu de inicio
				return "S"
				
	#si el primer elemento (ya sea M o F) es igual al sexo de la persona que está siendo buscada, OR esta ultima tiene sexo inderterminado
	elif ((sexoDeInteres[0]==sexo) or (sexo == "I")):
		if (rangoEdades[0] <= edad and rangoEdades[1] >= edad) and ((distanciaEntreDos (ubicacionUsuarioLogueado, ubicacion)) <= radioBusqueda):
			# si entra en el rango de edades # si la distancia entre los dos es menor a la especificado por el usuario, osea radioBusqueda
			porcentajeCoin = calcularPorcentaje (interesesUsuarioLogueado, intereses)
			print ("-"*40,"\n",usuarioElegido, "y tu tienen {}% de coincidencia".format (porcentajeCoin))

			#llama a la funcion opcionesBusqueda
			if (opcionesBusqueda (usuarioElegido))=="S":	# si puso salir, vuelve al menu de inicio
				return "S"
				
	else:
		usuarioElegido=""	#igualmente, si no cumple ninguna de las condiciones, se "elimina" de la lista de gente a buscar
	
	
	
	

# dados el numero de usuario
def opcionesBusqueda(usuarioElegido):

	eleccionUsuario = input ("""
	¿Que deseas hacer?
	Dar Like(L)
	Salir(S) 
	Ignorar(Cualquier Tecla)
	""")

	if eleccionUsuario.upper() == "L":
		if usuarioElegido in datos[ejecucionActual["pseu"]]["likes"]:	#si la persona está en la lista de likes del usuario logueado
			eleccion = input("El usuario '{}' te likeó, ¿Quieres dejarle un mensaje? (S/N)".format(usuarioElegido))
			if eleccion.upper() == "S":
				
				guardarMensajes(usuarioElegido)
				usuarioElegido=""	# de la lista "elimina" al usuario actual de la busqueda
				
			else:  # si su eleccion fue N
				usuarioElegido=""
				return print("No le dejaste ningun mensaje")
		else:  # si no està en la lista de likes
			guardarLikes(usuarioElegido)
			
			usuarioElegido=""
			return print("Le diste like ❤")

	elif eleccionUsuario.upper() == "S":
		return "S"

	else:  # si el usuario apreta cualquier tecla, osea si lo ignora
		usuarioElegido=""

		
		
#---------------BLOQUE GUARDAR MENSAJES-----------------------
def guardarMensajes(usuarioElegido):
	mensaje = str (input ("Dejale un mensaje: "))
	
	#se fija si el usuario pertenece al csv o al pickle
	if usuarioElegido in ejecucionActual["usuariosPredefinidos"]:
		guardarMensajesCSV(usuarioElegido, ejecucionActual["pseu"],mensaje)
	else:
		guardarMensajesPICKLE(usuarioElegido, ejecucionActual["pseu"],mensaje)


		


		
		
#va a guardar en el archivo csv, dados "usuarioDeLaBusqueda,usuarioLogueado(juanito),listDeUsuarioBusqueda=[juanito,["te deje un mensaje"]]"
def guardarMensajesCSV(usuarioBusqueda, userLogueado, nuevoMensaje):
	#lee el archivo entero y va guardando cada linea en una lista, cuando encuentra al usuario, lo guarda en esta lista pero con la informacion nueva, luego guarda cada elemento de la lista en el mismo archivo, reemplazando lo que tenia antes
	#LECTURA
	with open(r"usuariosPredefinidos.csv","r") as usuariosCsv:
		usuariosCsv.seek(0)
		pseudonimo,nombre,apellido,contraseña,sexo,edad,latitud,longitud, intereses, likes,mensajes = leer_archivo(usuariosCsv)
		guardarInfo=[]
		while pseudonimo:
			if pseudonimo==usuarioBusqueda: #si en la lectura encuentra al usuario, para asi acceder a su base de datos
				dicAActualizar=deTextoADiccionario(mensajes)	#una var. que almacena el casteo del diccionario
				#tiene esta pinta {'fem': ['hola todo bien', 'chau nos vimos'], 'juanita': ['hola te deje un mensaje']}
				#checkea que haya algun elemento en el diccionario
				if (userLogueado not in dicAActualizar):
					dicAActualizar[userLogueado]=[nuevoMensaje]	#si el dic esta vacio
					datos[usuarioBusqueda]["mensajes"][userLogueado]=[nuevoMensaje]
				else:
					dicAActualizar[userLogueado].append(nuevoMensaje)
					datos[usuarioBusqueda]["mensajes"][userLogueado].append(nuevoMensaje)
				dicActualizadoYCasteado=deDiccionarioATexto(dicAActualizar)	#transofrma el diccionario en el formato para guardar, en string
				guardarLineas = "{0};{1};{2};{3};{4};{5};{6};{7};{8};{9};{10}\n".format(pseudonimo, nombre,apellido,contraseña,sexo,edad,latitud,longitud, intereses, likes, dicActualizadoYCasteado)
				guardarInfo.append(guardarLineas)
				
				#vuelve a leer
				pseudonimo,nombre,apellido,contraseña,sexo,edad,latitud,longitud, intereses, likes,mensajes = leer_archivo(usuariosCsv)
			else:
				guardarLineas = "{0};{1};{2};{3};{4};{5};{6};{7};{8};{9};{10}\n".format(pseudonimo, nombre,apellido,contraseña,sexo,edad,latitud,longitud, intereses, likes, mensajes)
				guardarInfo.append(guardarLineas)
				#vuelve a leer
				pseudonimo,nombre,apellido,contraseña,sexo,edad,latitud,longitud, intereses, likes,mensajes = leer_archivo(usuariosCsv)
	#ESCRITURA	
	with open(r"usuariosPredefinidos.csv","w") as guardarUsuariosCsv:
		for info in guardarInfo:
			guardarUsuariosCsv.write("{}".format(info))
			
			
		
	
#modifica un valor del pickle y vuelve a dejar en el orden en el que estaba el archivo
def guardarMensajesPICKLE(usuarioBusqueda, userLogueado, nuevoMensaje):
	with open(r"nuevosUsuarios.pkl","rb") as usuariosPickle:
		guardarDatosPickle=[]
		try:
			while True:
				datosUsuario=load(usuariosPickle)
				pseudonimo=datosUsuario[0]
				dicDeMensajes=datosUsuario[1]["mensajes"]
				if usuarioBusqueda==pseudonimo:
					if (userLogueado not in dicDeMensajes):
						dicDeMensajes[userLogueado]=[nuevoMensaje]
						datos[usuarioBusqueda]["mensajes"][userLogueado]=[nuevoMensaje]
					else:
						dicDeMensajes[userLogueado].append(nuevoMensaje)
						datos[usuarioBusqueda]["mensajes"][userLogueado].append(nuevoMensaje)
						
					guardarDatosPickle.append(datosUsuario)
				else:
					guardarDatosPickle.append(datosUsuario)
		except EOFError:
			pass
	with open(r"nuevosUsuarios.pkl","wb") as guardarPickle:	#vuelve a guardar todos los datos en el pickle
		for Usuarios in guardarDatosPickle:
			dump(Usuarios,guardarPickle)	
			
			
		
		
	
	
		
		
		
#-------------GUARDAR LIKES--------------------
def guardarLikes(usuarioElegido):
	if usuarioElegido in ejecucionActual["usuariosPredefinidos"]:
		guardarLikesCSV(usuarioElegido, ejecucionActual["pseu"])
	else:
		guardarLikesPICKLE(usuarioElegido, ejecucionActual["pseu"])
	datos[usuarioElegido]["likes"].append(ejecucionActual["pseu"]) #actualiza la info al diccionario "datos"

		
		
#los likes se almacenan asi "usuario1,juanita,usuario1,usuario3"
def guardarLikesCSV(usuarioBusqueda, userLogueado):
	#lee el archivo entero y va guardando cada linea en una lista, cuando encuentra al usuario, lo guarda en esta lista pero con la informacion nueva, luego guarda cada elemento de la lista en el mismo archivo
	#LECTURA
	with open(r"usuariosPredefinidos.csv","r") as usuariosCsv:
		pseudonimo,nombre,apellido,contraseña,sexo,edad,latitud,longitud, intereses, likes,mensajes = leer_archivo(usuariosCsv)
		guardarInfo=[]
		while pseudonimo:
			if pseudonimo==usuarioBusqueda: #si en la lectura encuentra al usuario
				listLikesUserBusq=likes.split(",")	#lo transforma en formato lista
				listLikesUserBusq.append(userLogueado)	#añade al usuario logueado a la lista de likes de la persona
				guardarFormato=",".join(listLikesUserBusq) #lo guarda en este formato "usuario1,juanita,usuario1,usuario3"
				guardarLineas = "{0};{1};{2};{3};{4};{5};{6};{7};{8};{9};{10}\n".format(pseudonimo, nombre,apellido,contraseña,sexo,edad,latitud,longitud, intereses, guardarFormato, mensajes)
				guardarInfo.append(guardarLineas)
				
				#vuelve a leer
				pseudonimo,nombre,apellido,contraseña,sexo,edad,latitud,longitud, intereses, likes,mensajes = leer_archivo(usuariosCsv)
			else:
				#separa todo y lo guarda en la lista
				guardarLineas = "{0};{1};{2};{3};{4};{5};{6};{7};{8};{9};{10}\n".format(pseudonimo, nombre,apellido,contraseña,sexo,edad,latitud,longitud, intereses, likes, mensajes)
				guardarInfo.append(guardarLineas)
				#vuelve a leer
				pseudonimo,nombre,apellido,contraseña,sexo,edad,latitud,longitud, intereses, likes,mensajes = leer_archivo(usuariosCsv)
	#ESCRITURA	
	with open(r"usuariosPredefinidos.csv","w") as guardarUsuariosCsv:
		for info in guardarInfo:
			guardarUsuariosCsv.write("{}".format(info))
	
	
	
#recodar que en el pickle los datos se guardan ["pseu",{"nombre":"juanito",...}]
def guardarLikesPICKLE(userLectura, userAGuardar):
	with open(r"nuevosUsuarios.pkl","rb") as usuariosPickle:
		guardarDatosPickle=[]	#va a terminar siendo una lista de listas
		
		try:
			while True:
				datosUsuario=load(usuariosPickle)	#es la lista con los 2 elementos
				userr=datosUsuario[0]
				if userLectura==userr:
					datosUsuario[1]["likes"].append(userAGuardar)
					guardarDatosPickle.append(datosUsuario)
				else:
					guardarDatosPickle.append(datosUsuario)
		except EOFError:
			pass
		
	#una vez que guardo todo en la lista, a cada elemento lo pone en el pickle
	with open(r"nuevosUsuarios.pkl","wb") as guardarPickle:	#vuelve a guardar todos los datos en el pickle
		for Usuarios in guardarDatosPickle:
			dump(Usuarios,guardarPickle)
		
		
		

	
	


#---------------------BLOQUE CONTESTAR MENSAJES------------------------	
def interfazMensajes():
	opcionesMensajes=""
	while opcionesMensajes!="2":
		opcionesMensajes = input ("""
(1) MOSTRAR CHATS
(2) VOLVER
Escriba el numero de opcion deseada: 
""")
		if opcionesMensajes=="1":
			return mostrarChats()
			


def mostrarChats():
	userLogueado=ejecucionActual["pseu"]
	dicMensajes=datos[userLogueado]["mensajes"]
	usuariosDelChat=list(dicMensajes.keys())
	
	if usuariosDelChat:	
		for usuarios in usuariosDelChat:	#imprime todos los chats
			print("\t",usuarios)
		personaElegida=input("\nCon quien deseas hablar?")
		while personaElegida not in usuariosDelChat:
			print("No tiene una conversacion con ese usuario")
			personaElegida=input("\nCon quien deseas hablar?")
		mostrarConversacion(personaElegida,userLogueado)
	else:	#si la lista usuariosDelChat esta vacia
		return print("No tienes ningun mensaje")
	
	
	
def mostrarConversacion(personaElegida, userLogueado):
	msgsRecibidos=datos[userLogueado]["mensajes"][personaElegida]
	if userLogueado not in datos[personaElegida]["mensajes"]:	#si solamente recibió un mensaje
		print(personaElegida,": ",msgsRecibidos[0])
		opcionesConversacion(personaElegida, userLogueado)
	else:	#si ambos ya tenian una conversacion
		msgsEnviados=datos[personaElegida]["mensajes"][userLogueado]		
		for msg in intercalarListasConPrefijo(msgsRecibidos,msgsEnviados,personaElegida,userLogueado):
			print(msg)
		opcionesConversacion(personaElegida, userLogueado)
	

	
	
	
#dadas dos listas de cualquier long. ["1", "2", "3", "4","5","6"] y ["a", "b", "c", "d"] y un nombre1 "aa" y un nombre2 "bb"
# devuelve -> ['aa: 1', 'bb: a', 'aa: 2', 'bb: b', 'aa: 3', 'bb: c', 'aa: 4', 'bb: d', 'aa: 5', 'aa: 6']
def intercalarListasConPrefijo(lista1, lista2,name1,name2):
	c=[]
	num=0
	a=lista1[:]  #tener en cuenta que "remove" elimina elementos de la lista original	
	b=lista2[:]
	while a or b:
		if a:
		
			c.append("".join([name1,": ",a[num]]))
			a.remove(a[num])
		if b:
			c.append("".join([name2,": ",b[num]]))
			b.remove(b[num])
	return c
			
	
	
	
def opcionesConversacion(personaElegida, userLogueado):
	print("(1) CONTESTAR\n(2) VOLVER")
	eleccion=input("Que deseas hacer?")
	while eleccion!="1" and eleccion!="2":
		print("Vamos, por favor...estoy cansado....")
		eleccion=input("Que deseas hacer?")
	if eleccion=="1":
		guardarMensajes(personaElegida)
	return
	


		
#---------------BLOQUE CREACION USUARIO Y VALIDACIONES------------------		
def crearUsuario():
	nombreDeUsuario = verificarUsuario()
	contraseña=verificarContraseña()
	edad=verificarEdad()
	sexo=verificarSexo()
	nombre = str (input ("Ingrese su/s nombre/s: "))
	apellido = str (input ("Ingrese su/s apellido/s: "))
	longitud = float(input ("ingrese latitud (entre -90 y 90): "))
	latitud = float(input ("ingrese longitud (entre -90 y 90): "))
	intereses = str (input ("Ingrese sus intereses o hobbies separados por espacios y guiones. Ej.: 'gatos viajar museos-de-arte: "))
	intereses = intereses.split(" ")

		
	datosUsuarioReg= {
		"nombre": nombre,
		"apellido": apellido,
		"contraseña": contraseña,
		"sexo": sexo,
		"edad": edad,
		"ubicacion": [longitud, latitud],
		"intereses": intereses,
		"likes":[],
		"mensajes": {}}
		
	#------ guarda los datos en el archivo pickle, como diccionarios
	with open(r"nuevosUsuarios.pkl","ab") as registrarNuevoUsuario:	#notar que esta en modo "append"
		dump([nombreDeUsuario,datosUsuarioReg],registrarNuevoUsuario)	#guarda la info en el pickle en forma de lista. [psudonimo,{datosUsuario}]
	ordenarPickle()
	
	datos[nombreDeUsuario]=datosUsuarioReg	#añade al diccionario datos
	ejecucionActual["listaUsers"].append(nombreDeUsuario)	#mete al usuario que se acaba de registrar, en la lista ejecucionActual["listaUsers"]
	
	
	return print ("Felicidades, ya es usuario de Tinder")



	
	

def validarContraseña(contraseña):
	# debe contener al menos una minúscula, una masyucula, un número y 5 caracteres")
	# la funcion any, se fija si dada una iteracion AL MENOS encuentra un elemeneto que sea verdadero
	# EJEMPLO print (any (i == "_" for i in "pseudonimo"))	# devuelve True si hay algun guion bajo
	# EJEMPLO islower(), verifica si un caracter es minuscula


	if (any (i in "!#$%&/()=?¡¿[]+-{}" for i in contraseña)):	#si hay alguno de esos caracteres, entonces pide ingresar de nuevo, cuando se la llamó a la funcion
		return False

	elif (len (contraseña) >= 5) and any (i.isdigit () for i in contraseña) and (any (i.isupper () for i in contraseña) and any (i.islower() for i in contraseña)):
		return True

	else:
		return False

#print (validarContraseña ("hosdaD5s!"))


def validarPseudonimo(pseudonimo):

	if any(i.isupper () for i in pseudonimo):
		return False
	
	elif (any (i in "!#$%&/()=?¡¿[]+-{}" for i in pseudonimo)):
		return False
		
	elif (any (i.isdigit () for i in pseudonimo)) or (any (i == "_" for i in pseudonimo)) or any (letra.islower () for letra in pseudonimo):
		#si entró a este elif, es porque no hay mayusculas, ni simbolos especiales
		return True	 # ("hay almenos un numero o un guion bajo o una minuscula")

	else:
		return False


	
def validarEdad(edad):
	return 18 <= edad <= 99


def verificarEdad():
	
	edad = int (input ("Ingrese su edad: "))
	
	while not validarEdad (edad):
		#print ("Debe tener entre 18 y 99 años para registrarse en el sistema.")
		print("ingrese una edad entre 18 o 99 años")
		edad = int (input ("Ingrese su edad: "))
	return edad
		
		
def verificarContraseña():
	contraseña = str (input ("Ingrese una contraseña: "))
	while not validarContraseña(contraseña):
		print ("Contraseña invalida, por favor ingrese una contraseña que contenga por lo menos una minúscula, un número, una mayúscula y 5 caracteres")
		contraseña = str (input ("Ingrese una contraseña: "))
	return contraseña

	
	
def verificarSexo():
	sexo = (str (input ("Sexo (seleccione M, F o I): "))).upper ()
	while (sexo != "M" and sexo != "F" and sexo != "I"):
		print ("vuelva a ingresar los datos")
		sexo = (str (input ("Sexo (seleccione M, F o I): "))).upper ()
	return sexo

	

def verificarUsuario():
	nombreDeUsuario=str (input ("Ingrese un nombre de usuario: "))
	
	while (nombreDeUsuario in ejecucionActual["listaUsers"]) or (not validarPseudonimo (nombreDeUsuario)):
		if (nombreDeUsuario in ejecucionActual["listaUsers"]):
			nombreDeUsuario = str (input ("Usuario ya existente, intente con uno diferente: "))
		
		if not validarPseudonimo (nombreDeUsuario):
			nombreDeUsuario = str (input ("Usuario invalido, por favor ingrese un usuario que contenga únicamente minúsculas, números o guión bajo."))
	   
	return nombreDeUsuario
			


			
#--------------ORDENAMIENTO DEL ARCHIVO PICKLE----------------------
def ordenarPickle():	#guarda en una lista cada elemento del pickle y luego hace un sort de la lista, y guarda nuevamente en el pickle
	#lee los datos
	archivoPickleLectura = open('nuevosUsuarios.pkl', 'rb')
	try:
		nombreUsers=[]
		while True:
			usuarioPickle=load(archivoPickleLectura)	#load lee desde el inicio del pickle hasta el final
			nombreUsers.append(usuarioPickle)
	except EOFError:	#si se encuentra con el fin de archivo
		nombreUsers.sort(key=lambda x:x[0])	#ordena por el primer elemento, recordar que sort, modifica la lista original
	archivoPickleLectura.close()
	
	#graba cada elemento de la lista ordenada en el pickle
	archivoPickleActualizado = open('nuevosUsuarios.pkl', 'wb')	#modo sobreescritura
	for usuarioAOrdenar in nombreUsers:
		dump(usuarioAOrdenar,archivoPickleActualizado)
	archivoPickleActualizado.close()
	return
	

   
   
#------------------MERGE DE PICKLE Y CSV------------------  
def mergePickleCsv(archivoPickle, archivoCsv):	 #recibe un archivo en formato csv y uno en formato pickle y añade los datos al diccionarios "datos"
	#lee el pickle
	try:
		while True:
			usuariosEnPickle=load(archivoPickle)
			datos[usuariosEnPickle[0]]=usuariosEnPickle[1]	#recordar que los elementos se guardan asi: [pseu,{nombre:"manuel"...}]
	except EOFError:
		pass

	#lee el csv, y castea
	pseudonimo,nombre,apellido,contraseña,sexo,edad,latitud,longitud, intereses, likes,mensajes = leer_archivo(archivoCsv)
	while pseudonimo:
		datosUsuario= {
			"nombre": nombre,
			"apellido": apellido,
			"contraseña": contraseña,
			"sexo": sexo,
			"edad": int(edad),
			"ubicacion": [float(latitud),float(longitud)],
			"intereses": intereses.split(","),
			"likes": likes.split(","),
			"mensajes": deTextoADiccionario(mensajes),
			}
		
		datos[pseudonimo]=datosUsuario
		pseudonimo,nombre,apellido,contraseña,sexo,edad,latitud,longitud, intereses, likes,mensajes = leer_archivo(archivoCsv)
	return
	

		
	
	
#--------------------IMPRIMIR TODOS LOS USUARIOS--------------------	
def imprimirUsuarios(archivoCsv,archivoPkl):
	pseudonimoCSV, nombreCSV, apellidoCSV, edadCSV = leerArchivoCsv(archivoCsv)	
	pseudonimoPKL, nombrePKL, apellidoPKL, edadPKL = intentarLeerPickle(archivoPkl)
	separador="="*80
	print(separador)
	print("{:<20} {:^20} {:^20} {:>10}".format("USUARIO", "NOMBRE", "APELLIDO", "EDAD"))
	while (pseudonimoPKL and pseudonimoCSV):
		if (pseudonimoCSV<pseudonimoPKL):
			imprimirDatos(pseudonimoCSV, nombreCSV, apellidoCSV, edadCSV)
			pseudonimoCSV, nombreCSV, apellidoCSV, edadCSV = leerArchivoCsv(archivoCsv)
		else:
			imprimirDatos(pseudonimoPKL, nombrePKL, apellidoPKL, edadPKL)
			pseudonimoPKL, nombrePKL, apellidoPKL, edadPKL = intentarLeerPickle(archivoPkl)
				
	while (pseudonimoCSV):
		imprimirDatos(pseudonimoCSV, nombreCSV, apellidoCSV, edadCSV)
		pseudonimoCSV, nombreCSV, apellidoCSV, edadCSV = leerArchivoCsv(archivoCsv)
		
	while (pseudonimoPKL):	#si aun hay algo en el pkl, que lo imprima
		imprimirDatos(pseudonimoPKL, nombrePKL, apellidoPKL, edadPKL)
		pseudonimoPKL, nombrePKL, apellidoPKL, edadPKL = intentarLeerPickle(archivoPkl)
	print(separador)
		
		
def imprimirDatos(dato1, dato2, dato3, dato4):
	print("{:<20} {:^20} {:^20} {:>10}".format(dato1, dato2, dato3, dato4))

	
def intentarLeerPickle(archivoPkl):
	try:
		pseudonimoPKL, nombrePKL, apellidoPKL, edadPKL = leerArchivoPickle(archivoPkl)
		return pseudonimoPKL, nombrePKL, apellidoPKL, edadPKL
	except EOFError:
		return (False,False,False,False)	#para que sea posible el desempaquetamiento
	

def leerArchivoPickle(archivoPickle):
	datosUsuarioPKL=load(archivoPickle)
	
	pseudonimoPKL=datosUsuarioPKL[0]
	nombrePKL=datosUsuarioPKL[1]["nombre"]
	apellidoPKL=datosUsuarioPKL[1]["apellido"]
	edadPKL=datosUsuarioPKL[1]["edad"]
	return pseudonimoPKL, nombrePKL, apellidoPKL, edadPKL
	
	
	
def leerArchivoCsv(archivoCsv):
	pseudonimoCSV,nombreCSV,apellidoCSV,contraseña,sexo,edadCSV,latitud,longitud, intereses, likes,mensajes = leer_archivo(archivoCsv)
	return pseudonimoCSV, nombreCSV, apellidoCSV, edadCSV
			
	
	

	
	
	

#--------------------OTRAS FUNCIONES--------------------
def top5():
	losTopFive=[0,0,0,0,0]
	losTopFiveNombres=["","","","",""]
	for usuarios in ejecucionActual["listaUsers"]:
		cantLikesDelUser = len(datos[usuarios]["likes"])
		posicion=0	#establece el contador de posicion en 0.
		while posicion<5:
			if cantLikesDelUser>losTopFive[posicion]: #va comparando las primeras 5 posiciones de losTopFive
				losTopFive.insert(posicion,cantLikesDelUser)
				losTopFiveNombres.insert(posicion,usuarios)
				posicion=5	#corta el ciclo while
			else:
				posicion+=1	#vuelve a empezar el while, pero esta vez en la siguiente posicion
		
	return losTopFive[0:5],losTopFiveNombres[0:5]	#devuelve una tupla, con dos listas dentro
	

	
	
def definirSexoInt():
	sexoInteres = (str (input ("Ingrese el/los sexo/s de interes (M, F o A):"))).upper()
	while sexoInteres not in ["M","F","A"]:
		print ("Por favor ingrese una de las opciones: sexo masculino ('M'), sexo femenino ('F') o ambos ('A')")
		sexoInteres = (str (input ("Ingrese el/los sexo/s de interes (M, F o A):"))).upper()
	if sexoInteres in ["F","M"]:
		return [sexoInteres]
	return ["M","F"]
	
	

# ej. de texto para transformar a dic. => "fem!! [hola todo bien, jajja]|| juanita!! [hola te deje un mensaje]"
def deTextoADiccionario(texto):
	dic={}
	if len(texto)>5:	#solo si el texto tiene mas de 5 caracteres
		msgSeparado=texto.split("||")
		for charla in msgSeparado:
			mensajeDe=charla.split("!!")
			psuSinEspacio=mensajeDe[0].strip(" ")
			conversacionSinEspacio=mensajeDe[1].strip("][ ")
			dic[psuSinEspacio]=conversacionSinEspacio.split(",")
		return dic
	else:
		return {}
		
		

		
		
#transforma un diccionario de esta forma
# {'fem': ['hola todo bien','jajja'], 'juanita': ['hola te deje un mensaje']}
#a esta forma
# fem!! [hola todo bien, jajja]|| juanita!! [hola te deje un emensaje]"
def deDiccionarioATexto(diccionario):
	lista=[]
	# mensajesCadaUno=list(diccionario.values())	#lista de listas
	# cadaUsuario=list(diccionario.keys())	#lista de strings
	todo=list(diccionario.items())	#lista de tuplas 
	#[('fem', ['hola todo bien', ' ¿como me dijiste?', ' chau nos vimos']), ('juanita', ['hola te deje un emensaje'])]
	
	for elementosTupla in todo:
		lista.append("{}!!{}".format(elementosTupla[0],elementosTupla[1]))
		
		lista.append("||")
	a="".join(lista).rstrip("||")
	return a.replace("'","")		
		
		
		
	
	
def calcularPorcentaje(interes1, interes2):	 # funcion que dadas dos listas, devuelve el porcentaje de coincidencia entre ambas
	acum = 0
	for ciclo in interes1:
		if ciclo in interes2:
			acum += 1
	return floor (((100 * acum) / (len (interes1) + len (interes2))))


# usando Vicenty (necesita geopy)
def distanciaEntreDos(distancia1, distancia2):
	# dadas dos distancias(variable que contiene una lista), devuelve la distancia en km
	return vincenty (distancia1, distancia2).km

	
		
def leer_archivo(archivo):
	linea = archivo.readline()	#lee la siguiente linea gracias al readline, que luego de usar este comando, se deja en la posicion en la que estaba el archivo
	if linea:	#si la linea tiene texto...
		linea = linea.strip("\n")	#toma la linea entera y le quita el \n
	else:	#si la linea está vacia
		linea = ";;;;;;;;;;"	
	return linea.split(";") #devuelve una lista, con todos los valores separados
	
	
def leerUsuariosCsv():	#devuelve una lista de los usuarios en el csv
	with open(r"usuariosPredefinidos.csv","r") as datosCsv:
		pseudonimo,nombre,apellido,contraseña,sexo,edad,latitud,longitud, intereses, likes,mensajes = leer_archivo(datosCsv)
		usuariosCsv=[]
		while pseudonimo:
			usuariosCsv.append(pseudonimo)
			pseudonimo,nombre,apellido,contraseña,sexo,edad,latitud,longitud, intereses, likes,mensajes = leer_archivo(datosCsv)
	return usuariosCsv


	
# print ("\n" * 100) una manera de limpiar la pantalla






#-------------------------BLOQUE PRINCIPAL--------------------------
datos={}	#diccionario donde se almacenan todos los usuarios

ejecucionActual={
	"pseu":"",	#va a contener el nombre del usuario que esté activo en el sistema
	"listaUsers":[],
	"usuariosPredefinidos":[]
	}



nuevosUsuarios=open(r"nuevosUsuarios.pkl","rb")
usuariosPredefinidos=open(r"usuariosPredefinidos.csv","r")

mergePickleCsv(nuevosUsuarios,usuariosPredefinidos) #al hacer el merge actualiza los datos de cada archivo al diccionario "datos"

ejecucionActual["listaUsers"]=list(datos.keys()) #asigna a listaUsers una lista, que tiene como elementos todos los valores del diccionario "datos"
ejecucionActual["usuariosPredefinidos"]=leerUsuariosCsv()

nuevosUsuarios.close()
usuariosPredefinidos.close()

#despues de hacer cosas con los archivos llama a la funcion principal
menuPrincipal()







