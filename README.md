## Dependencies

Creating virtual environment

    python3 -m venv venv

Activating virtual environment

    source venv/bin/activate

You can confirm you’re in the virtual environment by checking the location of your Python interpreter:

    which python

As long as your virtual environment is activated `pip` will install packages into that specific environment, and you’ll be able
to import and use packages in your Python application.

Installing dependencies from requirements.txt
    
    python3 -m pip install -r requirements.txt

### Mininet

According to [Mininet documentation](http://mininet.org/download/), you can install Mininet by running the following commands:

    sudo apt update
    sudo apt install mininet

### Pox

[Pox](https://github.com/noxrepo/pox) is already imported in this repository. We are actually using the _gar-experimental_ release which
is the latest stable version supporting Python 3. If you encounter any issues, you can try using the _fangtooth_ release which
supports Python 2.

### Iperf

[Iperf](https://iperf.fr/) comes pre-installed on Ubuntu or any Debian-based distribution.

## Running the topology

To run the topology, run the following commands:

First:

    chmod +x ./scripts/*

Then, start the controller:

    ./scripts/start-firewall-with-rules.sh

Finally, on a separate terminal, start the topology:

    ./scripts/start-topo.sh 2

At this point, you should be able to see the topology running on Mininet. The first parameter refers to the number of switches. `pingall` on the mininet CLI should run 
successfully.

