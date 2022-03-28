# Se instala imagen de ubuntu para trabajar con python y mariadb
FROM ubuntu:20.04

#Actualizamos los repos y descargamos maria db
RUN apt-get update
RUN apt-get install -y mariadb-server

#exponemos el puerto de mariadb 3306
EXPOSE 3306

#informacion adicional para la imagen
LABEL version="1.0"
LABEL description="MariaDB Server"


HEALTHCHECK --start-period=5m \
  CMD mariadb -e 'SELECT @@datadir;' || exit 1

#Actualizamos e instalamos python3 
 RUN apt-get update \
  && apt-get install -y python3-pip python3-dev python3.7 \
  && cd /usr/local/bin \
  && ln -s /usr/bin/python3 python \
  && pip3 install --upgrade pip

#Creamos la carpeta en donde se alojara el proyecto
WORKDIR /app
#Copiamos los archivos del proyecto a la carpeta creada
COPY . /app
#Instalamos los paquetes que necesita el proyecto para corres
RUN pip3 --no-cache-dir install -r requirements.txt

#Bloque de configuracion maria db
#iniciamos el servicio de mariadb
RUN /etc/init.d/mysql start

#Ingresamos a maria db y creamos y subimos el respaldo de la base de datos 
RUN /bin/bash -c "/usr/bin/mysqld_safe --skip-grant-tables &" && \
  sleep 5 && \
  mysql -u root -e "CREATE DATABASE db_customers" && \
  mysql -u root db_customers < db_customers.sql

#Reiniciamos el servicio y agregamos contrasena al usuario root, cambiamos permisos para archivos de mysql o mariadb
 RUN /etc/init.d/mysql restart
 RUN /bin/bash  service mysql start  && \ 
   mysql && \
   chmod 777 /var/run/mysqld/mysqld.sock && \
  mysql -u root -e "SET PASSWORD FOR 'root'@'localhost' = PASSWORD('root')"

#nombramos como se llamara la imagen inicial
CMD ["python3","src/app.py"]