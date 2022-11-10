from mininet.topo import Topo


class Topology(Topo):
    def build(self, n_switches=2):
        if n_switches < 1:
            print("Error: n_switches must be greater than 0")
            exit(-1)

        print("Starting Topology with %s switches" % (n_switches))
        hosts = []
        
        # Necesitamos 4 hosts (los 2 de cada extremo)
        for i in range(1, 5):
            print("Adding host: host_%s" % (i))
            hosts.append(self.addHost("host_%s" % i, ip="10.0.0.%s" % i))
        
        # Agregamos los switches, pero no los conectamos todavia
        switches = []
        for i in range(1, n_switches + 1):
            print("Adding switch: switch_%s" % (i))
            switches.append(self.addSwitch("switch_%s" % i))

        # Conectamos los switches entre si
        for i in range(n_switches - 1):
            print("Adding link between: switch_{} and switch_{}".format(i, i+1))
            self.addLink(switches[i], switches[i + 1])

        # Conectamos los hosts a los switches, donde el h1 y h2 se conectan al s1, h3 y h4 al sN
        # (donde N es el ultimo switch)
        print("Adding link between: host_1 and switch_1")
        self.addLink(hosts[0], switches[0])

        print("Adding link between: host_2 and switch_1")
        self.addLink(hosts[1], switches[0])

        print("Adding link between: host_3 and switch_%s" % (n_switches))
        self.addLink(hosts[2], switches[-1])

        print("Adding link between: host_4 and switch_%s" % (n_switches))
        self.addLink(hosts[3], switches[-1])


topos = {"topologia": Topology}
