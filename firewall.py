from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.revent.revent import EventMixin
from pox.lib.util import dpidToStr
from pox.lib.packet.ethernet import ethernet
from pox.lib.packet.ipv4 import ipv4
from pox.lib.addresses import EthAddr
import json


def parse_json(path):
    with open(path) as file:
        data = json.load(file)
    return data


log = core.getLogger()
# Por defecto, tomamos que al switch al cual se le van a aplicar las reglas es el 1
topo_switch_id = 1
rules = {"rules": []}


class Firewall(EventMixin):
    def __init__(self):
        self.listenTo(core.openflow)
        log.debug("Enabling Firewall Module")

    def _handle_ConnectionUp(self, event):
        if event.dpid == topo_switch_id:
            for rule in rules["rules"]:
                msg = of.ofp_flow_mod()
                self.add_rule(msg, rule)
                event.connection.send(msg)
            log.debug(
                "Firewall rules installed on %s - switch %i",
                dpidToStr(event.dpid),
                topo_switch_id,
            )

    def add_rule(self, msg, rule):
        if "tcp" in rule:
            self.add_tcp_rule(rule["tcp"], msg)
        if "udp" in rule:
            self.add_udp_rule(rule["udp"], msg)
        if "ip" in rule:
            self.add_ip_rule(rule["ip"], msg)
        if "mac" in rule:
            self.add_mac_rule(rule["mac"], msg)

    def add_tcp_rule(self, rule, msg):
        msg.match.dl_type = ethernet.IP_TYPE
        msg.match.nw_proto = ipv4.TCP_PROTOCOL
        if "src_port" in rule:
            msg.match.tp_src = rule["src_port"]
            log.debug(
                "Rule installed: dropping packet TCP to port %i", rule["src_port"]
            )
        if "dst_port" in rule:
            msg.match.tp_dst = rule["dst_port"]
            log.debug(
                "Rule installed: dropping packet TCP to port %i", rule["dst_port"]
            )

    def add_udp_rule(self, rule, msg):
        msg.match.dl_type = ethernet.IP_TYPE
        msg.match.nw_proto = ipv4.UDP_PROTOCOL
        if "src_port" in rule:
            msg.match.tp_src = rule["src_port"]
            log.debug(
                "Rule installed: dropping packet UDP to port %i", rule["src_port"]
            )
        if "dst_port" in rule:
            msg.match.tp_dst = rule["dst_port"]
            log.debug(
                "Rule installed: dropping packet UDP to port %i", rule["dst_port"]
            )

    def add_ip_rule(self, rule, msg):
        msg.match.dl_type = ethernet.IP_TYPE
        if "src_ip" in rule:
            msg.match.nw_src = rule["src_ip"]
            log.debug(
                "Rule installed: dropping packet from IP address %s", rule["src_ip"]
            )
        if "dst_ip" in rule:
            msg.match.nw_dst = rule["dst_ip"]
            log.debug(
                "Rule installed: dropping packet to IP address %s", rule["dst_ip"]
            )

    def add_mac_rule(self, rule, msg):
        if "src_mac" in rule:
            msg.match.dl_src = EthAddr(rule["src_mac"])
            log.debug("Rule installed: dropping packet from MAC %s", rule["src_mac"])
        if "dst_mac" in rule:
            msg.match.dl_dst = EthAddr(rule["dst_mac"])
            log.debug("Rule installed: dropping packet to MAC %s", rule["dst_mac"])

    def _handle_PacketIn(self, event):
        pass


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
