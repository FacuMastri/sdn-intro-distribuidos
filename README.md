# Trabajo Práctico 2: Software-Defined Networks

## Dependencias

Creando entorno virtual:

    python3 -m venv venv

Activando el entorno virtual:

    source venv/bin/activate

Se puede confirmar si el entorno virtual está activado con el comando:

    which python

Mientras se esté trabajando en el entorno virtual, `pip` va a instalar las dependencias de Python en el directorio `venv`,
y se podrán usar e importar en los scripts de Python.

Instalando dependencias desde `requirements.txt`:

    python3 -m pip install -r requirements.txt


### Mininet

De acuerdo a la [documentación de Mininet](http://mininet.org/download/), se puede instalar Mininet corriendo los siguientes comandos:

    sudo apt update
    sudo apt install mininet

### Pox

[Pox](https://github.com/noxrepo/pox) se encuentra incluido en este repositorio. Actualmente, estamos usando el release de  _gar-experimental_
el cual es la última versión estable que soporta Python 3. Si se encuentra algún inconveniente, se puede intentar usar el release de _fangtooth_.
que soporta Python 2.

### Iperf

[Iperf](https://iperf.fr/) viene preinstalado en Ubuntu o en cualquiera distribución de Linux basada en Debian.

### Xterm

Xterm sirve para poder abrir una terminal dentro de un host de Mininet. Se puede instalar con el siguiente comando:

    sudo apt install xterm


## Ejecutando la topología

Para ejecutar la topología, se debe ejecutar los siguientes comandos:

Primero:

    chmod +x ./scripts/*

Luego, levantar el controlador:

    ./scripts/firewall-with-rules.sh

Finalmente, en una terminal diferente, ejecutar la topología:

    ./scripts/topo.sh 2

En este punto, se debe poder ver la topología corriendo dentro de Mininet. El primer parámetro de 
`topo.sh` es la cantidad de switches que se quieren utilizar.

## Scripts y pruebas

Para levantar las terminales de los nodos:

    xterm host_1 host_4

Para levantar un servidor en el puerto <port> con TCP:

    iperf -s -p <port>

Para levantar un cliente: 

    iperf -c 10.0.0.4 -p <port>