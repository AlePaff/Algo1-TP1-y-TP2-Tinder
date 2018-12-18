# from math import radians, cos, sin, asin, sqrt  # para la harvensine
from math import floor
from geopy.distance import vincenty	 # instalar geopy, ejecutar desde la consola   tambien funciona con "great_circle"
from pickle import dump, load
from ast import literal_eval



#----------------------BLOQUE MENU------------------------
def menuPrincipal():
	opcionesMenuPrincipal = ""	#inicializa la variable
	
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
			nuevosUsuarios00=open(r"nuevosUsuario.pkl","rb")
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
			interfazMensajes(ejecucionActual["pseu"])
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

	sexoInteres = str (input ("Ingrese el/los sexo/s de interes (M, F o A):"))
	sexoInt = definirSexoInt (sexoInteres)

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
	
	# recorre la longitud de LA COPIA de la lista de usuarios, para evitar el problema de out of range
	for numUser in range (len(ejecucionActual["listaUsers"])):
		# va a repetirse las veces como numero de usuario haya y va a recorrer la lista de usuarios
		# las variables de aca abajo cambian en cada iteracion

		# en datos, ejecucionActual["listaUsers"][numUser] es un string, en este caso, un pseudonimo
		usuarioElegido=ejecucionActual["listaUsers"][numUser]
		
		sexo = datos[usuarioElegido]["sexo"]	 
		ubicacion = datos[usuarioElegido]["ubicacion"]
		edad = datos[usuarioElegido]["edad"]
		intereses = datos[usuarioElegido]["intereses"]
		
		# para el caso que busco H y M, osea si hay dos elementos en la lista "sexoDeInteres"
		if ((len (sexoDeInteres)) == 2 or (sexo == "I")):
			if (rangoEdades[0] <= edad and rangoEdades[1] >= edad) and ((distanciaEntreDos (ubicacionUsuarioLogueado, ubicacion)) <= radioBusqueda):
				porcentajeCoin = calcularPorcentaje (interesesUsuarioLogueado, intereses)
				print (usuarioElegido, " y tu tienen {} % de coincidencia".format (porcentajeCoin))
	   
				#llama a la funcion opcionesBusqueda
				if (opcionesBusqueda (usuarioElegido))=="S":	# si puso salir, vuelve al menu de inicio
					ejecucionActual["listaUsers"]=copiaListaUsers
					return
					
		#si el primer elemento (ya sea M o F) es igual al sexo de la persona que está siendo buscada, OR esta ultima tiene sexo inderterminado
		elif ((sexoDeInteres[0]==sexo) or (sexo == "I")):
			if (rangoEdades[0] <= edad and rangoEdades[1] >= edad) and ((distanciaEntreDos (ubicacionUsuarioLogueado, ubicacion)) <= radioBusqueda):
				# si entra en el rango de edades # si la distancia entre los dos es menor a la especificado por el usuario, osea radioBusqueda
				porcentajeCoin = calcularPorcentaje (interesesUsuarioLogueado, intereses)
				print (usuarioElegido, " y tu tienen {} % de coincidencia".format (porcentajeCoin))

				#llama a la funcion opcionesBusqueda
				if (opcionesBusqueda (usuarioElegido))=="S":	# si puso salir, vuelve al menu de inicio
					ejecucionActual["listaUsers"]=copiaListaUsers
					return
					
		else:
			usuarioElegido=""	#igualmente, si no cumple ninguna de las condiciones, se "elimina" de la lista de gente a buscar
	
	ejecucionActual["listaUsers"]=copiaListaUsers
	return print ("La busqueda ha finalizado.")


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
			eleccion = input ("El usuario {} te likeó, ¿quieres dejarle un mensaje? (S/N)").format (usuarioElegido)
			if eleccion.upper() == "S":
				
				guardarMensajes(usuarioElegido)
				usuarioElegido=""	# de la lista "elimina" al usuario actual de la busqueda
				
			else:  # si su eleccion fue N
				usuarioElegido=""
				return print("No le dejaste ningun mensaje")
		else:  # si no està en la lista de likes
		
			guardarLikes(usuarioElegido)
			datos[usuarioElegido]["likes"].append(ejecucionActual["pseu"]) #añade a la lista de likes de la persona, al usuario actual
					
			usuarioElegido=""
			return print("Le diste like")

	elif eleccionUsuario.upper() == "S":
		return "S"

	else:  # si el usuario apreta cualquier tecla, osea si lo ignora
		usuarioElegido=""

		
		
#---------------BLOQUE GUARDAR MENSAJES Y LIKES-----------------------
def guardarMensajes(usuarioElegido):
	mensaje = [str (input ("Dejale un mensaje: "))]	#crea una lista
	usuarioYMensaje={ejecucionActual["pseu"]:mensaje}	#crea un diccionario, que tiene como clave el usuario actual, y valor una lista con el mensaje que le dejó el usuario
	#si pertenece a la lista de usuarioPredefinidos, osea al archivo csv
	if usuarioElegido in ejecucionActual["usuariosPredefinidos"]:
		guardarMensajesCSV(usuarioElegido, ejecucionActual["pseu"],usuarioYMensaje)
		print("hasta aca?")
	else:
		guardarMensajesPICKLE(usuarioElegido, ejecucionActual["pseu"],usuarioYMensaje)


#va a guardar en el archivo csv, dados dos usuarios y un mensaje
def guardarMensajesCSV(userLectura, userAGuardar, dictMensaje):
	with open(r"usuariosPredefinidos.csv","r+") as usuariosCsv:
		usuariosCsv.seek(0)
		pseudonimo,nombre,apellido,contraseña,sexo,edad,latitud,longitud, intereses, likes,mensajes = leer_archivo(usuariosCsv)
		castearMensaje=literal_eval(mensajes)	#castearMensaje es un diccionario
		while pseudonimo:
			if pseudonimo==userLectura:
				castearMensaje.update(dictMensaje)
				linea = "{0};{1};{2};{3};{4};{5};{6};{7};{8};{9};{10}\n".format(pseudonimo, nombre,apellido,contraseña,sexo,edad,latitud,longitud, intereses, likes, castearMensaje)
				usuariosCsv.write(linea)
				
				pseudonimo,nombre,apellido,contraseña,sexo,edad,latitud,longitud, intereses, likes,mensajes = leer_archivo(usuariosCsv)
				castearMensaje=literal_eval(mensajes)
			else:
				pseudonimo,nombre,apellido,contraseña,sexo,edad,latitud,longitud, intereses, likes,mensajes = leer_archivo(usuariosCsv)
	return
	
#modifica un valor del pickle y vuelve a dejar en el orden en el que estaba el archivo
def guardarMensajesPICKLE(userLectura, userAGuardar, dictMensaje):
	with open(r"nuevosUsuario.pkl","rb") as usuariosPickle:
		guardarDatosPickle=[]
		try:
			while True:
				pseudonimo=load(usuariosPickle)
				userr=list(pseudonimo.keys())[0]
				if userLectura==userr:
					pseudonimo[userr]["mensajes"][userAGuardar].update(dictMensaje)
					guardarDatosPickle.append(pseudonimo)
				else:
					guardarDatosPickle.append(pseudonimo)
		except EOFError:
			pass
	with open(r"nuevosUsuario.pkl","wb") as guardarPickle:	#vuelve a guardar todos los datos en el pickle
		for Usuarios in guardarDatosPickle:
			dump(Usuarios,guardarPickle)	
			
		

def guardarLikes(usuarioElegido):
	if usuarioElegido in ejecucionActual["usuariosPredefinidos"]:
		guardarLikesCSV(usuarioElegido, ejecucionActual["pseu"])
	else:
		guardarLikesPICKLE(usuarioElegido, ejecucionActual["pseu"])

		
		
#los likes se almacenan asi ['usuario1', 'juanita', 'usuario1', 'usuario3']
def guardarLikesCSV(userLectura, userAGuardar):
	with open(r"usuariosPredefinidos.csv","w+") as usuariosCsv:
		usuariosCsv.seek(0)
		
		pseudonimo,nombre,apellido,contraseña,sexo,edad,latitud,longitud, intereses, likes,mensajes = leer_archivo(usuariosCsv)
		castearLikes=literal_eval(likes)
		
		while pseudonimo:
			if pseudonimo==userLectura:
				print(pseudonimo, userLectura)
				castearLikes.append(userAGuardar)
				linea = "{0};{1};{2};{3};{4};{5};{6};{7};{8};{9};{10}\n".format(pseudonimo, nombre,apellido,contraseña,sexo,edad,latitud,longitud, intereses, castearLikes, mensajes)
				usuariosCsv.write(linea)
				
				pseudonimo,nombre,apellido,contraseña,sexo,edad,latitud,longitud, intereses, likes,mensajes = leer_archivo(usuariosCsv)
				castearLikes=literal_eval(likes)
			else:
				pseudonimo,nombre,apellido,contraseña,sexo,edad,latitud,longitud, intereses, likes,mensajes = leer_archivo(usuariosCsv)
	
	
def guardarLikesPICKLE(userLectura, userAGuardar):
	with open(r"nuevosUsuario.pkl","rb") as usuariosPickle:
		guardarDatosPickle=[]
		
		try:
			while True:
				pseudonimo=load(usuariosPickle)	#es el diccionario entero
				userr=list(pseudonimo.keys())[0]	#es un string
				if userLectura==userr:
					pseudonimo[userr]["likes"].append(userAGuardar)
					guardarDatosPickle.append(pseudonimo)	#guarda el diccionario entero en una lista
				else:
					guardarDatosPickle.append(pseudonimo)
		except EOFError:
			pass
			
	#una vez que guardo todo en la lista, a cada elemento lo pone en el pickle
	with open(r"nuevosUsuario.pkl","wb") as guardarPickle:	#vuelve a guardar todos los datos en el pickle
		for Usuarios in guardarDatosPickle:
			dump(Usuarios,guardarPickle)
		
		
		

	
	


#---------------------BLOQUE CONTESTAR MENSAJES------------------------	
def interfazMensajes(userLogueado):
	archivoCsv=open(r"usuariosPredefinidos.csv","r")
	if userLogueado in ejecucionActual["usuariosPredefinidos"]:	#si el usuario logueado pertenece al archivo csv
		if mostrarMensajesCSV(archivoCsv, userLogueado):
			return True
			
	else:
		archivoPkl=open(r"nuevosUsuario.pkl","rb")
		if mostrarMensajesPKL(archivoPkl,userLogueado):
			return True
	

	
def mostrarMensajesCSV(archivoCsv,userLogueado):
	pseu, nombre, apellido, edad, mensajes = leerArchivoCsv(archivoCsv)
	while pseu:
		if pseu==userLogueado and mensajes:	#mensajes, es un diccionario
			archivoCsv.close()
			verContestarMensajes(mensajes)
			return True
		pseu, nombre, apellido, edad, mensajes = leerArchivoCsv(archivoCsv)
	return print("No tienes ningun mensaje")


	
def mostrarMensajesPKL(archivoPkl, userLogueado):
	try:
		pseu, nombre, apellido, edad, mensajes = leerArchivoPickle(archivoPkl)
		while pseu:
			if pseu==userLogueado and mensajes:	#mensajes es un diccionario
				archivoPkl.close()
				verContestarMensajes(mensajes)
				return True
			pseu, nombre, apellido, edad, mensajes = leerArchivoPickle(archivoPkl)
	except EOFError:
		return print("No tienes ningun mensaje")
	
	
def verContestarMensajes(dicConListasDentro):
	for users in dicConListasDentro:	#recorre cada clave del diccionario
		print("Tienes un mensaje de:", users)
		print(dicConListasDentro[users][-1])	#muestra el ultimo mensaje
		elec=input("Deseas contestarle? S/N \n")
		if elec.upper()=="S":
			guardarMensajes(users)	#esta funcion se encarga de decidir si el usuario pertenece al pickle o al csv
		
	
	
	
	
		

   
   
   
	

		
#---------------BLOQUE CREACION USUARIO Y VALIDACIONES------------------		
def crearUsuario():
	nombreDeUsuario = verificarUsuario()
	contraseña=verificarContraseña()
	edad=verificarEdad()
	sexo=verificarSexo()
	nombre = str (input ("Ingrese su/s nombre/s: "))
	apellido = str (input ("Ingrese su/s apellido/s: "))
	longitud = int (input ("ingrese latitud (entre -90 y 90): "))
	latitud = int (input ("ingrese longitud (entre -90 y 90): "))
	intereses = str (input ("Ingrese sus intereses o hobbies separados por espacios y guiones. Ej.: 'gatos viajar museos-de-arte: "))
	intereses = intereses.split(" ")

	datosDelUsuario = {
		nombreDeUsuario: {
			"nombre": nombre,
			"apellido": apellido,
			"contraseña": contraseña,
			"sexo": sexo,
			"edad": edad,
			"ubicacion": [longitud, latitud],
			"intereses": intereses,
			"likes":[],
			"mensajes": {}
		}}
		
	#------ guarda los datos en el archivo pickle
	with open(r"nuevosUsuario.pkl","ab") as registrarNuevoUsuario:	#notar que esta en modo "append"
		dump(datosDelUsuario,registrarNuevoUsuario)	#guarda la info, en el pickle
	ordenarPickle()
	
	ejecucionActual["listaUsers"].append(nombreDeUsuario)	#mete al usuario que se acaba de registrar, en la lista ejecucionActual["listaUsers"]
	datos.update (datosDelUsuario)	 # mete el diccionario "datosDelUsuario", dentro de "datos"
	
	return print ("Felicidades, ya es usuario de Tinder")


def definirSexoInt(sexoInteres):
	if sexoInteres.upper() == "M":
		sexoInt = ["M"]
	elif sexoInteres.upper() == "F":
		sexoInt = ["F"]
	elif sexoInteres.upper() == "A":
		sexoInt = ["M", "F"]
	else:
		print ("Por favor ingrese una de las opciones: sexo masculino ('M'), sexo femenino ('F') o ambos ('A')")
		sexoInteres = input ("Ingrese el sexo de interes: ")
		definirSexoInt (sexoInteres)
		sexoInt = ""
	return sexoInt
	
	

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
	archivoPickleLectura = open('nuevosUsuario.pkl', 'rb')
	try:
		lista=[]
		while True:
			usuarioPickle=load(archivoPickleLectura)	#load lee desde el inicio del pickle hasta el final
			lista.append(usuarioPickle)
	except EOFError:	#si se encuentra con el fin de archivo
		nuevaLista=lista
	
		#para ordenar por pseudonimo
		# print(lista)
		# for diccionarios in lista:
			# for pseuUser in list(diccionarios.items()):
				# ordenar=pseuUser[0]
		
		# nuevaLista = sorted(lista, key=lambda k: k[ordenar])
		
	archivoPickleLectura.close()
	
	#graba cada elemento de la lista ordenada en el pickle
	archivoPickleActualizado = open('nuevosUsuario.pkl', 'wb')	#modo sobreescritura
	for usuarioAOrdenar in nuevaLista:
		dump(usuarioAOrdenar,archivoPickleActualizado)
	archivoPickleActualizado.close()

	
	#si leo el archivo pickle ordenado...
	# ppickled_file = open('nuevosUsuario.pkl', 'rb')
	# try:
		# while True:
			# print(load(ppickled_file))
	# except EOFError:
		# pass
		
	return
	

   
   
#------------------MERGE DE PICKLE Y CSV------------------  
def mergePickleCsv(archivoPickle, archivoCsv):	 #recibe un archivo en formato csv y uno en formato pickle y devuelve un diccionario, de ambos
	mergeDeAmbos={}
	
	#lee el pickle
	try:
		while True:
			usuariosEnPickle=load(archivoPickle)
			mergeDeAmbos.update(usuariosEnPickle)
	except EOFError:
		pass

		#lee el csv, y castea
	pseudonimo,nombre,apellido,contraseña,sexo,edad,latitud,longitud, intereses, likes,mensajes = leer_archivo(archivoCsv)
	while pseudonimo:
		user = {
		pseudonimo: {
			"nombre": nombre,
			"apellido": apellido,
			"contraseña": contraseña,
			"sexo": sexo,
			"edad": int(edad),
			"ubicacion": [float(latitud),float(longitud)],
			"intereses": intereses.split(","),
			"likes":literal_eval(likes),
			#otra forma mas complicada seria   likes.replace("'","").replace(" ","").strip("][")
			"mensajes": literal_eval(mensajes),
			}}
			
		#literal_eval convierte un texto, un str, en lo que sea que represente en python
		#por ejemplo el texto "{'clave':33}", que esta en formato str lo convierte en un diccionario
		mergeDeAmbos.update(user)
		pseudonimo,nombre,apellido,contraseña,sexo,edad,latitud,longitud, intereses, likes,mensajes = leer_archivo(archivoCsv)
	return mergeDeAmbos
	


	
	
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
	

def imprimirUsuarios(archivoCsv,archivoPkl):
	try:
		pseudonimoPKL, nombrePKL, apellidoPKL, edadPKL, mensajesPKL = leerArchivoPickle(archivoPkl)
		pseudonimoCSV, nombreCSV, apellidoCSV, edadCSV, mensajes = leerArchivoCsv(archivoCsv)	
		
		while (pseudonimoPKL and pseudonimoCSV):
			if (pseudonimoCSV<pseudonimoPKL):
				print(pseudonimoCSV, nombreCSV, apellidoCSV, edadCSV)
				pseudonimoPKL, nombrePKL, apellidoPKL, edadPKL, mensajesPKL = leerArchivoPickle(archivoPkl)
				pseudonimoCSV, nombreCSV, apellidoCSV, edadCSV, mensajes = leerArchivoCsv(archivoCsv)
			else:
				print(pseudonimoPKL, nombrePKL, apellidoPKL, edadPKL)
				pseudonimoPKL, nombrePKL, apellidoPKL, edadPKL, mensajesPKL = leerArchivoPickle(archivoPkl)
				pseudonimoCSV, nombreCSV, apellidoCSV, edadCSV, mensajes = leerArchivoCsv(archivoCsv)
				
		while (pseudonimoPKL):	#si aun hay algo en el pkl, que lo imprima
			print(pseudonimoPKL, nombrePKL, apellidoPKL, edadPKL)
			pseudonimoPKL, nombrePKL, apellidoPKL, edadPKL, mensajesPKL = leerArchivoPickle(archivoPkl)
			
		while (pseudonimoCSV):
			print(pseudonimoCSV, nombreCSV, apellidoCSV, edadCSV)
			pseudonimoCSV, nombreCSV, apellidoCSV, edadCSV, mensajes = leerArchivoCsv(archivoCsv)
	
	except EOFError:
		pass
	return 
	
		
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

	
def leerArchivoPickle(archivoPickle):
	dictPKL=load(archivoPickle)	#carga el diccionario de una entrada del pickle en dictPKL
	pseudonimoPKL=list(dictPKL.keys())[0]	#se fija el que tiene como clave (osea que nombre de usuario tiene)
	nombrePKL=dictPKL[pseudonimoPKL]["nombre"]
	apellidoPKL=dictPKL[pseudonimoPKL]["apellido"]
	edadPKL=dictPKL[pseudonimoPKL]["edad"]
	mensajesPKL=dictPKL[pseudonimoPKL]["mensajes"]
	return pseudonimoPKL, nombrePKL, apellidoPKL, edadPKL, mensajesPKL
	
	
def leerArchivoCsv(archivoCsv):
	pseudonimoCSV,nombreCSV,apellidoCSV,contraseña,sexo,edadCSV,latitud,longitud, intereses, likes,mensajes = leer_archivo(archivoCsv)
	return pseudonimoCSV, nombreCSV, apellidoCSV, edadCSV, literal_eval(mensajes)
		
		
def leer_archivo(archivo):
	linea = archivo.readline()	#lee la siguiente linea gracias al readline, que luego de usar este comando, se deja en la posicion en la que estaba el archivo
	if linea:	#si la linea tiene texto...
		linea = linea.strip("\n")	#toma la linea entera y le quita el \n
	else:	#si la linea está vacia
		linea = ";;;;;;;;;;"	
	return linea.split(";") #devuelve una lista, con todos los valores separados
	
	



	
# print ("\n" * 100) una manera de limpiar la pantalla






#-------------------------BLOQUE PRINCIPAL--------------------------
datos={}	#diccionario donde se almacenan todos los usuarios

ejecucionActual={
	"pseu":"",	#va a contener el nombre del usuario que esté activo en el sistema
	"listaUsers":[],
	"usuariosPredefinidos":["asd", "juanita", "usuario1", "usuario2", "usuario3", "jhon", "unaUsuaria", "ind", "mascu", "fem"]
	}



nuevosUsuarios=open(r"nuevosUsuario.pkl","rb")
usuariosPredefinidos=open(r"usuariosPredefinidos.csv","r")

datosResultantes=mergePickleCsv(nuevosUsuarios,usuariosPredefinidos) #merge entre pickle y diccionario, a un unico diccionario llamado datos
datos.update(datosResultantes)	 #actuliza el diccionario resultante al diccionario datos

ejecucionActual["listaUsers"]=list(datos.keys()) #asigna a listaUsers una lista, que tiene como elementos todos los valores del diccionario "datos"

nuevosUsuarios.close()
usuariosPredefinidos.close()

#despues de hacer cosas con los archivos llama a la funcion principal
menuPrincipal()







