from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.revent.revent import EventMixin
from pox.lib.util import dpidToStr
from pox.lib.packet.ethernet import ethernet
from pox.lib.packet.ipv4 import ipv4
from pox.lib.addresses import EthAddr
import json


def parse_json(path):
    try:
        with open(path) as file:
            data = json.load(file)
        return data
    except Exception:
        log.error("Exception while parsing json file")
        exit(-1)

log = core.getLogger()
# Por defecto, tomamos que al switch al cual se le van a aplicar las reglas es el 1
topo_switch_id = 1
rules = None


class Firewall(EventMixin):
    def __init__(self):
        self.listenTo(core.openflow)
        log.debug("Enabling Firewall Module")

    def _handle_ConnectionUp(self, event):
        # Instalamos el firewall en el primer switch
        if event.dpid == topo_switch_id:
            for rule in rules["rules"]:
                if rule["name"] == "pto_1":
                    self.drop_packet_on_port(event, rule["protocol"], rule["dst_port"])
                elif rule["name"] == "pto_2":
                    self.drop_packet_on_port_and_ip(
                        event, rule["dst_port"], rule["src_ip"], rule["protocol"]
                    )
                elif rule["name"] == "pto_3":
                    self.drop_packet_between_hosts(
                        event, rule["src_mac"], rule["dst_mac"]
                    )
            log.debug(
                "Firewall rules installed on %s - switch %i",
                dpidToStr(event.dpid),
                topo_switch_id,
            )

    def drop_packet_on_port(self, event, protocol, dst_port):
        """
        Se deben descartar todos los mensajes cuyo puerto de destino sea 80
        """
        msg = of.ofp_flow_mod()
        self._add_dst_port(msg, dst_port, protocol)
        event.connection.send(msg)
        log.debug(
            "Rule installed: dropping packets on dst_port %i and %s",
            dst_port,
            protocol.upper(),
        )

    def drop_packet_on_port_and_ip(self, event, dst_port, src_ip, protocol):
        """
        Se deben descartar todos los mensajes que provengan del host 1, tengan como puerto destino el 5001, y esten
        utilizando el protocolo UDP.
        """
        msg = of.ofp_flow_mod()
        msg.match.nw_src = src_ip
        self._add_dst_port(msg, dst_port, protocol)
        event.connection.send(msg)
        log.debug(
            "Rule installed: dropping packets from host IP %s, dst_port %i and UDP",
            src_ip,
            dst_port,
        )

    def _add_dst_port(self, msg, dst_port, protocol):
        msg.match.tp_dst = dst_port
        msg.match.dl_type = ethernet.IP_TYPE
        if protocol == "tcp":
            msg.match.nw_proto = ipv4.TCP_PROTOCOL
        else:
            msg.match.nw_proto = ipv4.UDP_PROTOCOL

    def drop_packet_between_hosts(self, event, src_mac, dst_mac):
        """
        Se debe elegir dos hosts cualquiera, y los mismos no deben poder comunicarse de ninguna forma.
        """
        msg = of.ofp_flow_mod()
        msg.match.dl_src = EthAddr(src_mac)
        msg.match.dl_dst = EthAddr(dst_mac)
        event.connection.send(msg)
        log.debug(
            "Rule installed: dropping packets from host MAC %s to host MAC %s",
            src_mac,
            dst_mac,
        )


def launch(rules_path, switch_id=1):
    if int(switch_id) < 1:
        log.error("Invalid switch id")
        exit(-1)
    global topo_switch_id
    global rules
    data = parse_json(rules_path)
    rules = data
    log.debug("Rules loaded:\n" + str(rules))
    topo_switch_id = int(switch_id)
    core.registerNew(Firewall)
