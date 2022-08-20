from datos_prueba import datos
from datos_prueba import diccionarioPrueba
from datos_prueba import ejecucionActual
from math import floor
# from math import radians, cos, sin, asin, sqrt  # para la harvensine
from geopy.distance import vincenty  # instalar geopy, ejecutar desde la consola   tambien funciona con "great_circle"


pseu = ""  # se la define globalmente, para despues usarla en las distintas funciones
listaUsers = []  # es una lista de usuarios global, la cual se actualiza con las claves de los diccionarios, cuando se carga el grupo de persona predeterminado


# print ("\n" * 100) una manera de limpiar la pantalla

def menuPrincipal():
    opcionesMenuPrincipal = ""  #inicializa la variable
    
    while opcionesMenuPrincipal!="4":
        opcionesMenuPrincipal = input ("""
(1) CARGAR UN GRUPO DE PERSONAS PREDETERMINADO
(2) CREAR CUENTA NUEVA
(3) INGRESAR AL SISTEMA
(4) CERRAR PROGRAMA
Escriba el numero de opcion deseada: 
""")
        if opcionesMenuPrincipal == "1":
            datos.update (diccionarioPrueba)    #va a añadir diccionarioPrueba al diccionario "datos", si hay valores iguales, los va a actualizar
            ejecucionActual["listaUsers"]=list(datos.keys()) #asigna a listaUsers una lista, que tiene como elementos todos los valores del diccionario "datos"
            
        elif opcionesMenuPrincipal == "2":
            crearUsuario () # llama una func, la cual sirve para cargar datos, y esto aladirlos al diccionario principal, osea a "datos"
            
        elif opcionesMenuPrincipal == "3":
            ingresarSistema ()
        elif opcionesMenuPrincipal=="4":    #se pone esta opciones porque sino, iría directo al else, y saldria del programa, pero mostrrando el cartel "por favor ingrese una...."
            return
        else:
            print ("Por favor, ingrese una de las opciones")

    



def ingresarSistema():

    ejecucionActual["pseu"] = str (input ("Ingrese su nombre de usuario:"))
    if ejecucionActual["pseu"] in ejecucionActual["listaUsers"]:
        contraseña = input ("Ingrese su contraseña: ")
        if contraseña == datos[ejecucionActual["pseu"]]["contraseña"]:
            print ("Bienvenide a Tinder", datos[ejecucionActual["pseu"]]["nombre"])
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
            a,b,c=filtrarBusquedas()    #la funcion filtrarBusquedas, devuelve 3 variables
            hacerBusqueda(a,b,c)    #hacerBusqueda necesita 3 parametros
            
        elif opcionesMenuSecundario == "2":
            mostrarMensajes()
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
    copiaListaUsers=ejecucionActual["listaUsers"][:]    #crea una copia, para actualizarla a la original mas tarde
    
    if ejecucionActual["pseu"] in ejecucionActual["listaUsers"]:    #el if, es por si hizo una segunda busqueda
        ejecucionActual["listaUsers"].remove(ejecucionActual["pseu"])  # elimina de la lista de usuarios, el usuario logueado (para que no aparezca él mismo en la busqueda)
        
    ubicacionUsuarioLogueado = datos[ejecucionActual["pseu"]]["ubicacion"]
    interesesUsuarioLogueado = datos[ejecucionActual["pseu"]]["intereses"]
    
    # recorre la longitud de LA COPIA de la lista de usuarios, para evitar el problema de out of range
    for numUser in range (len(ejecucionActual["listaUsers"])):
        # va a repetirse las veces como numero de usuario haya y va a recorrer la lista de usuarios
        # las variables de aca abajo cambian en cada iteracion

        sexo = datos[ejecucionActual["listaUsers"][numUser]]["sexo"]     # en datos, ejecucionActual["listaUsers"][numUser] es un string, en este caso, un pseudonimo
        ubicacion = datos[ejecucionActual["listaUsers"][numUser]]["ubicacion"]
        edad = datos[ejecucionActual["listaUsers"][numUser]]["edad"]
        intereses = datos[ejecucionActual["listaUsers"][numUser]]["intereses"]
        
        # para el caso que busco H y M, osea si hay dos elementos en la lista "sexoDeInteres"
        if ((len (sexoDeInteres)) == 2 or (sexo == "I")):
            if (rangoEdades[0] <= edad and rangoEdades[1] >= edad) and ((distanciaEntreDos (ubicacionUsuarioLogueado, ubicacion)) <= radioBusqueda):
                porcentajeCoin = calcularPorcentaje (interesesUsuarioLogueado, intereses)
                print (ejecucionActual["listaUsers"][numUser], " y tu tienen {} % de coincidencia".format (porcentajeCoin))
       
                #llama a la funcion opcionesBusqueda
                if (opcionesBusqueda (numUser))=="S":   # si puso salir, vuelve al menu de inicio
                    ejecucionActual["listaUsers"]=copiaListaUsers
                    return
                    
        #si el primer elemento (ya sea M o F) es igual al sexo de la persona que está siendo buscada, OR esta ultima tiene sexo inderterminado
        elif ((sexoDeInteres[0]==sexo) or (sexo == "I")):
            if (rangoEdades[0] <= edad and rangoEdades[1] >= edad) and ((distanciaEntreDos (ubicacionUsuarioLogueado, ubicacion)) <= radioBusqueda):
                # si entra en el rango de edades # si la distancia entre los dos es menor a la especificado por el usuario, osea radioBusqueda
                porcentajeCoin = calcularPorcentaje (interesesUsuarioLogueado, intereses)
                print (ejecucionActual["listaUsers"][numUser], " y tu tienen {} % de coincidencia".format (porcentajeCoin))

                #llama a la funcion opcionesBusqueda
                if (opcionesBusqueda (numUser))=="S":   # si puso salir, vuelve al menu de inicio
                    ejecucionActual["listaUsers"]=copiaListaUsers
                    return
                    
        else:
            ejecucionActual["listaUsers"][numUser]=""   #igualmente, si no cumple ninguna de las condiciones, se "elimina" de la lista de gente a buscar
    
    ejecucionActual["listaUsers"]=copiaListaUsers
    return print ("La busqueda ha finalizado.")

#NOTA: puede que la condicion de validarEdad y distanciaEntreDos esté duplicada, pero es mejor eso, que hacer otra funcion y pasarle un monton de parametros
    

    

# dados el numero de usuario y la eleccion...
def opcionesBusqueda(numeroDeUser):

    eleccionUsuario = input ("""
    ¿Que deseas hacer?
    Dar Like(L)
    Salir(S) 
    Ignorar(Cualquier Tecla)
    """)

    if eleccionUsuario.upper() == "L":
        if ejecucionActual["listaUsers"][numeroDeUser] in datos[ejecucionActual["pseu"]]["likes"]:  #si la persona está en la lista de likes del usuario logueado
            eleccion = input ("El Usuario {} te likeó, ¿quieres dejarle un mensaje? (S/N)").format (ejecucionActual["listaUsers"][numeroDeUser])
            if eleccion.upper() == "S":
                mensaje = str (input ("Dejale un mensaje: "))
                usuarioYMensaje={ejecucionActual["pseu"]:mensaje}   #crea un diccionario, que tiene como clave el usuario actual, y valor el mensaje que le dejó el usuario
                datos[ejecucionActual["listaUsers"][numeroDeUser]]["mensajes"].update(usuarioYMensaje)  #actualiza el diccionario "mensajes" del usuario que está siendo buscado, es decir, al cual se le dejó el mensaje
                ejecucionActual["listaUsers"][numeroDeUser]=""  # de la lista "elimina" al usuario actual de la busqueda
                
            else:  # si su eleccion fue N
                ejecucionActual["listaUsers"][numeroDeUser]=""
                return print("No le dejaste ningun mensaje")
        else:  # si no està en la lista de likes
            datos[ejecucionActual["listaUsers"][numeroDeUser]]["likes"].append(ejecucionActual["pseu"]) #añade a la lista de likes de la persona, al usuario actual
                    
            ejecucionActual["listaUsers"][numeroDeUser]=""
            return print("Le diste like")

    elif eleccionUsuario.upper() == "S":
        return "S"

    else:  # si el usuario apreta cualquier tecla, osea si lo ignora
        ejecucionActual["listaUsers"][numeroDeUser]=""

        
        

        
        
def calcularPorcentaje(interes1, interes2):  # funcion que dadas dos listas, devuelve el porcentaje de coincidencia entre ambas
    acum = 0
    for ciclo in interes1:
        if ciclo in interes2:
            acum += 1
    return floor (((100 * acum) / (len (interes1) + len (interes2))))

    

def mostrarMensajes():#hacer un while que vaya mostrando todos los mensajes que tiene el usuario
    if datos[ejecucionActual["pseu"]]["mensajes"]:
        for mensajitos in range(len(list(datos[ejecucionActual["pseu"]]["mensajes"].values()))):
            print ("\ntienes un mensaje de: ", list(datos[ejecucionActual["pseu"]]["mensajes"].keys())[mensajitos])
            print ("'",list(datos[ejecucionActual["pseu"]]["mensajes"].values())[mensajitos],"'")
    else:
        print ("No tiene ningún mensaje.")



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


   
   
   
def verificarUsuario():
    nombreDeUsuario=str (input ("Ingrese un nombre de usuario: "))
    
    while (nombreDeUsuario in ejecucionActual["listaUsers"]) or (not validarPseudonimo (nombreDeUsuario)):
        if (nombreDeUsuario in ejecucionActual["listaUsers"]):
            nombreDeUsuario = str (input ("Usuario ya existente, intente con uno diferente: "))
        
        if not validarPseudonimo (nombreDeUsuario):
            nombreDeUsuario = str (input ("Usuario invalido, por favor ingrese un usuario que contenga únicamente minúsculas, números o guión bajo."))
       
    return nombreDeUsuario
            
    

        
        
        
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
    ejecucionActual["listaUsers"].append(nombreDeUsuario)   #mete al usuario que se acaba de registrar en la lista ejecucionActual["listaUsers"]
    datos.update (datosDelUsuario)   # mete el diccionario datosDelUsuario, dentro de datos
    
    return print ("Felicidades, ya es usuario de Tinder")

    
    
    

def validarContraseña(contraseña):
    # debe contener al menos una minúscula, una masyucula, un número y 5 caracteres")
    # la funcion any, se fija si dada una iteracion AL MENOS encuentra un elemeneto que sea verdadero
    # EJEMPLO print (any (i == "_" for i in "pseudonimo"))  # devuelve True si hay algun guion bajo
    # EJEMPLO islower(), verifica si un caracter es minuscula


    if (any (i in "!#$%&/()=?¡¿[]+-{}" for i in contraseña)):   #si hay alguno de esos caracteres, entonces pide ingresar de nuevo, cuando se la llamó a la funcion
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
        return True  # ("hay almenos un numero o un guion bajo o una minuscula")

    else:
        return False


    
    
def validarEdad(edad):
    return 18 <= edad <= 99


# usando Vicenty (necesita geopy)
def distanciaEntreDos(distancia1, distancia2):
    # dadas dos distancias(variable que contiene una lista), devuelve la distancia en km
    return vincenty (distancia1, distancia2).km



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
    
    

    

'''
#SUPER SISTEMA ANTI EXPLOSIONES
try: 
    menuPrincipal ()
except:
    print("\n\nHubo un error durante la ejecucion\nCerrando el programa")
'''

menuPrincipal()

