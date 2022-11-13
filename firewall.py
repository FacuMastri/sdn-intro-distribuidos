from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.revent.revent import EventMixin
from pox.lib.util import dpidToStr
from pox.lib.packet.ethernet import ethernet
from pox.lib.packet.ipv4 import ipv4
from pox.lib.addresses import EthAddr
import json

def parse_json():
    with open("rules.json") as data_file:
        data = json.load(data_file)
    return data

log = core.getLogger()
# Por defecto, tomamos que al switch al cual se le van a aplicar las reglas es el 1
topo_switch_id = 1


class Firewall(EventMixin):
    def __init__(self):
        self.listenTo(core.openflow)
        log.debug("Enabling Firewall Module")
        self.rules = parse_json()
        log.debug("Rules loaded:\n" + str(self.rules))

    def _handle_ConnectionUp(self, event):
        # Instalamos el firewall en el primer switch
        if event.dpid == switch_id:
            for rule in self.rules["rules"]:
                if rule["name"] == "pto_1":
                    self.drop_packet_on_port(event, rule["protocol"], rule["dst_port"])
                elif rule["name"] == "pto_2":
                    self.drop_packet_on_port_and_ip_udp(
                        event, rule["dst_port"], rule["src_ip"]
                    )
                elif rule["name"] == "pto_3":
                    self.drop_packet_between_hosts(
                        event, rule["src_mac"], rule["dst_mac"]
                    )
            log.debug("Firewall rules installed on %s - switch %i", dpidToStr(event.dpid), switch_id)

    def drop_packet_on_port(self, event, protocol, dst_port):
        """
        Se deben descartar todos los mensajes cuyo puerto de destino sea 80
        """
        msg = of.ofp_flow_mod()
        msg.match.tp_dst = dst_port
        msg.match.dl_type = ethernet.IP_TYPE
        if protocol == "tcp":
            msg.match.nw_proto = ipv4.TCP_PROTOCOL
        else:
            msg.match.nw_proto = ipv4.UDP_PROTOCOL
        event.connection.send(msg)
        log.debug("Rule installed: dropping packets on dst_port %i and %s", dst_port, protocol.upper())

    def drop_packet_on_port_and_ip_udp(self, event, dst_port, src_ip):
        """
        Se deben descartar todos los mensajes que provengan del host 1, tengan como puerto destino el 5001, y esten
        utilizando el protocolo UDP.
        """
        msg = of.ofp_flow_mod()
        msg.match.tp_dst = dst_port
        msg.match.dl_type = ethernet.IP_TYPE
        msg.match.nw_proto = ipv4.UDP_PROTOCOL
        msg.match.nw_src = src_ip
        event.connection.send(msg)
        log.debug("Rule installed: dropping packets from host IP %s, dst_port %i and UDP", src_ip, dst_port)

    def drop_packet_between_hosts(self, event, src_mac, dst_mac):
        """
        Se debe elegir dos hosts cualquiera, y los mismos no deben poder comunicarse de ninguna forma.
        """
        msg = of.ofp_flow_mod()
        msg.match.dl_src = EthAddr(src_mac)
        msg.match.dl_dst = EthAddr(dst_mac)
        event.connection.send(msg)
        log.debug("Rule installed: dropping packets from host MAC %s to host MAC %s", src_mac, dst_mac)


def launch(switch_id=1):
    if int(switch_id) < 1:
        log.error("Invalid switch id")
        exit(-1)
    global topo_switch_id
    topo_switch_id = int(switch_id)
    core.registerNew(Firewall)
