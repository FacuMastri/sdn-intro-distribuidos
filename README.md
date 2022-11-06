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

### Testing installation

Once you have all the dependencies and the Mininet package installed you can test your installation by running the following command:

    pox/pox.py samples.spanning_tree

And on a separate terminal:

    sudo mn --custom ./src/test-loop.py --topo mytopo --arp --mac --switch ovsk --controller remote --test pingall