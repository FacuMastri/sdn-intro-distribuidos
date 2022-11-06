from mininet.topo import Topo


class MyTopo(Topo):
    def __init__(self):
        # Initialize topology
        Topo.__init__(self)
        # Add hosts and switches
        left_host = self.addHost("h1")
        right_host = self.addHost("h2")
        left_switch = self.addSwitch("s1")
        right_switch = self.addSwitch("s2")
        mid1 = self.addSwitch("s3")
        mid2 = self.addSwitch("s4")
        # Add links
        self.addLink(left_host, left_switch)
        self.addLink(right_host, right_switch)
        self.addLink(left_switch, mid1)
        self.addLink(left_switch, mid2)
        self.addLink(right_switch, mid1)
        self.addLink(right_switch, mid2)


topos = {"mytopo": (lambda: MyTopo())}
