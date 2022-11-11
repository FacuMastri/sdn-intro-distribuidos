from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.revent.revent import EventMixin
from pox.lib.util import dpidToStr
from pox.lib.packet.ethernet import ethernet
from pox.lib.packet.ipv4 import ipv4
from pox.lib.addresses import EthAddr
from collections import namedtuple
import os


log = core.getLogger()


class Firewall(EventMixin):
    def __init__(self):
        self.listenTo(core.openflow)
        log.debug("Enabling Firewall Module")

    def _handle_ConnectionUp(self, event):
        self.drop_packet_on_port(event, 80)
        log.debug("Firewall rules installed on %s", dpidToStr(event.dpid))

    def drop_packet_on_port(self, event, port):
        """
        Se deben descartar todos los mensajes cuyo puerto de destino sea 80
        """
        msg = of.ofp_flow_mod()
        # IP con UDP
        msg.match.tp_dst = port
        msg.match.dl_type = ethernet.IP_TYPE
        msg.match.nw_proto = ipv4.UDP_PROTOCOL
        event.connection.send(msg)

        # IP con TCP
        msg = of.ofp_flow_mod()
        msg.match.tp_dst = port
        msg.match.dl_type = ethernet.IP_TYPE
        msg.match.nw_proto = ipv4.TCP_PROTOCOL
        event.connection.send(msg)




def launch():
    core.registerNew(Firewall)
