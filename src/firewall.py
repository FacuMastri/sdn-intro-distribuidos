from pox.pox.core import core
import pox.pox.openflow.libopenflow_01 as of
from pox.pox.lib.revent.revent import EventMixin
from pox.pox.lib.util import dpidToStr
from pox.pox.lib.addresses import EthAddr
from collections import namedtuple
import os


log = core.getLogger()
policyFile = "%s/pox/pox/misc/firewall-policies.csv" % os.environ["HOME"]


class Firewall(EventMixin):
    def __init__(self):
        self.listenTo(core.openflow)
        log.debug("Enabling Firewall Module")

    def _handle_ConnectionUp(self, event):
        """Add your logic here ..."""

        log.debug("Firewall rules installed on %s", dpidToStr(event.dpid))


def launch():
    """
    Starting the Firewall module
    """
    core.registerNew(Firewall)
