## Preguntas a responder

### 1. ¿Cuál es la diferencia entre un Switch y un router? ¿Qué tienen en común?

Un switch trabaja en la capa de enlace, mientras que un router lo hace en la capa de red, tanto en el plano de datos como el de control. Ademas, un router puede conectar dispositivos de diferentes redes, mientras que un switch solo puede conectar dispositivos de la misma red local. 

Por otro lado, ambos dispositivos tienen en común que son capaces de enrutar paquetes de datos, ofrecen conectividad entre dispositivos, y pueden determinar por donde tiene que salir un paquete en función de sus direcciones de origen y de destino.

### 2. ¿Cuál es la diferencia entre un Switch convencional y un Switch OpenFlow?

La diferencia entre un switch convencional y un switch OpenFlow es que en un switch convencional, las funcionalidades de la capa de datos y de la capa de control se realizan en el mismo dispositivo.

Sin embargo, en los switches OpenFlow el plano de control se realiza en un controlador externo, mientras que el plano de datos se realiza en el switch, y ambos se comunican por medio del protocolo OpenFlow. Esta metodología, conocida como SDN permite una mayor efectividad en el uso de los recursos de la red que en una red convencional.

### 3. ¿Se pueden reemplazar todos los routers de la Intenet por Switches OpenFlow? Piense en el escenario interASes para elaborar su respuesta

Si para responder nos basamos en nuestro conocimiento sobre el escenario interASes, podemos decir que los routers que permiten la comunicación tienen la obligación de implementar el protocolo BGP, por ende se necesitaría que cada dispositivo tenga una enorme cantidad de entradas BGP almacenadas. 

Luego el control centralizado que proponen los switches OpenFlow sirve para redes triviales, lo cual no nos sirve pensando en la masividad de internet, por lo cual decimos que si bien seria "posible" es poco probable que se pueda llevar a cabo en la realidad.
