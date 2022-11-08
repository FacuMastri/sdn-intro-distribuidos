import argparse
from mininet.net import Mininet
from mininet.node import RemoteController
from mininet.cli import CLI
from mininet.log import setLogLevel, info


def topology(n_switches: int):
    # Usamos el controlador remoto que luego lo configuramos con POX
    net = Mininet(controller=RemoteController)

    net.addController("c0")

    hosts = []
    # Necesitamos 4 hosts (los 2 de cada extremo)
    for i in range(1, 5):
        hosts.append(
            net.addHost("h%s" % i, ip="10.0.0.%s" % i, mac="00:00:00:00:00:0%s" % i)
        )

    # Agregamos los switches, pero no los conectamos todavia
    switches = []
    for i in range(1, n_switches + 1):
        switches.append(net.addSwitch("s%s" % i))

    # Conectamos los switches entre si
    for i in range(n_switches - 1):
        net.addLink(switches[i], switches[i + 1])

    # Conectamos los hosts a los switches, donde el h1 y h2 se conectan al s1, h3 y h4 al sN
    # (donde N es el último switch)
    net.addLink(hosts[0], switches[0])
    net.addLink(hosts[1], switches[0])
    net.addLink(hosts[2], switches[-1])
    net.addLink(hosts[3], switches[-1])

    net.start()

    return net


def main():
    setLogLevel("info")
    parser = argparse.ArgumentParser()
    parser.add_argument("--switches", help="Number of network switches", type=int, default=3)
    args = parser.parse_args()
    net = topology(args.switches)
    CLI(net)
    net.stop()


if __name__ == "__main__":
    main()
