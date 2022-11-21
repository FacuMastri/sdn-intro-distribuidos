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

Luego, levantar el controlador donde el primer parámetro indica el ID del switch al cual aplicar las reglas (en este
caso será el switch 1):

    ./scripts/firewall-with-rules.sh 1

Finalmente, en una terminal diferente, ejecutar la topología:

    ./scripts/topo.sh 2

En este punto, se debe poder ver la topología corriendo dentro de Mininet. El primer parámetro de 
`topo.sh` es la cantidad de switches que se quieren utilizar.

## Scripts y otros comandos

Se cuentan con una serie de scripts para facilitar la ejecución de la topología y el controlador.

### `firewall.sh`

Permite levantar el controlador de POX con una serie de reglas customizadas y con el ID del switch al cual aplicar las
reglas. En el caso de no especificar el switch ID, se tomará por defecto el valor 1.

    ./scripts/firewall.sh <switch-id> <rules-path>

### `firewall-with-rules.sh`

Similar a `firewall.sh`, permite levantar el controlador de POX con una serie de reglas por defecto para el trabajo práctico
(las que se encuentran en `rules.json`) y con el ID del switch al cual aplicar las reglas. En el caso de no especificar el switch ID,
se tomará por defecto el valor 1.

    ./scripts/firewall-with-rules.sh <switch-id>

### `pox.sh`

Permite levantar el controlador sin el firewall, es decir, se va a permitir todo tipo de tráfico.

    ./scripts/pox.sh

### `topo.sh`

Permite levantar la topología de Mininet con la cantidad de switches especificada. En el caso de no especificar la cantidad de switches,
se tomará por defecto el valor 2.

    ./scripts/topo.sh <number-of-switches>

### `xterm`

Para abrir una terminal dentro de un host de Mininet, se puede ejecutar el siguiente comando:

    xterm <host-name>

Por ejemplo, en nuestro caso si queremos tener una terminal dentro del host 1 y host 2, ejecutamos:

    xterm host_1 host_2

### `iperf`

Para realizar las diversas pruebas especificadas en el trabajo práctico, debemos levantar un servidor en un host
y un cliente en otro host.

Si queremos levantar un servidor, una vez abierta la terminal de xterm dentro de un host, ejecutamos:

    iperf -s -p <port> [-u]

En cambio, si queremos levantar un cliente: 

    iperf -c <ip-servidor> -p <port> [-u]

En ambos casos, el flag `-u` es opcional y sirve para indicar que se va a usar UDP en lugar de TCP. Además,
la IP de los hosts comienzan a partir de10.0.0.1, es decir, al host 1 le corresponde 10.0.0.1, al host 2 le corresponde
10.0.0.2, etc.