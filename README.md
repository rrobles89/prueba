# prueba
prueba tn

1)  Tener instalado python3.

2)  Descargar proyecto instalar todas las librerias de python que se encuentran en el archivo requrements.txt.

3)  Abrir un terminal o consola y ubicarse en la carpeta que contiene el proyecto  y ejecutar el archivo Dockerfile con el comando "docker build -t pruebatn ." 
    quitar las comillas , recordar que el demonio de docker esta arriba.
	
4)  Al ejecutar el dockerfile comenzara a descargar la imagen base, las dependencias, copiar el proyecto ,configurar y subir el respaldo de la base de datos

5)  Para crear el contendedor ejecutamos el siguiente comando "docker run -it --publish 7000:4000 -d pruebatn"

6) Para iniciar el servicio de mysql ejecutamos el siguiente comando  "docker exec -it <id_container>  bash service mysql start" en donde <id_container>  
   colocamos el id del  contendor que se esta corriendo.
   
7) accedemos a la url de la aplicación localhost:7000  que 7000 es el puerto que esta expuesto .

8) al acceder a la url http://localhost:7000/ se cargara la informacion del archivo de clientes a la  base de datos si es la priemra vez nos saldra un mensaje "Archivo Cargado"
   si es la segunda vez nos mostrara un mnesaje "El archivo ya fue cargado" se esta validando que si ya existe la informacion ya no se vuelva a cargar.
   
9)para ver la informacion http://localhost:7000/listado en donde mostrara los clientes cargados

10)para mostrar la informacion de un solo cliente http://localhost:7000/usuario/id en donde id es el id del cliente

11) para colocar la latitud y longitud se utliza la siguiente url http://localhost:7000/actualizar  se debe probar con postman 

 POST
 
solicitud
 {
    "id" : 20,
    "latitud" : "-0.1081339",
    "longitud" : "-78.4699519"
}

respuesta
{
    "response": "Se Actualizo Correctamente"
}


