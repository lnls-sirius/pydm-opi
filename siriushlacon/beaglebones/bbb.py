#!/usr/bin/python-sirius
import logging
import pickle
import os
import subprocess
import time
import json

import ipaddress
import copy

# from entities import Command, Node, Sector, Type, NodeState


class BBB:
    """
    A class to represent a Beaglebone host.
    """

    CONFIG_JSON_PATH = "/opt/device.json"

    def __init__(self, path="/var/tmp/bbb.bin", interface="eth0"):
        """
        Creates a new object instance.
        :param path: the configuration file's location
        """
        # Creates the objects that wrap the host's settings.
        self.node = Node()

        self.logger = logging.getLogger("BBB")

        #  Parameters that define absolute locations inside the host
        self.configuration_file_path = path

        # The interface used (ethernet port on the Beaglebone).
        self.interface_name = interface

        self.read_node_parameters()
        self.node.state = NodeState.CONNECTED
        self.node.state_string = NodeState.to_string(self.node.state)

        self.node.type = Type.from_code(Type.UNDEFINED)
        self.node.ip_address = str(ipaddress.ip_address(self.get_ip_address()[0]))

        self.current_config_json_mtime = None

        # Load the data from the cfg file.
        self.check_config_json()

    def check_config_json(self):
        """
        Verify if the version loaded of the file config.json is the lattest
        available. If not, load again.
        """
        if os.path.exists(BBB.CONFIG_JSON_PATH):
            config_json_mtime = os.path.getmtime(BBB.CONFIG_JSON_PATH)
            if (
                self.current_config_json_mtime is None
                or config_json_mtime != self.current_config_json_mtime
            ):
                with open(BBB.CONFIG_JSON_PATH, "r") as f:
                    config = json.load(f)
                    self.current_config_json_mtime = config_json_mtime
                    self.node.type.code = int(config["device"])
                    self.node.details = "{}\tbaudrate={}".format(
                        config["details"], config["baudrate"]
                    )
                    self.node.config_time = config["time"]

                    self.write_node_configuration()

    def get_current_config(self):
        """
        Returns a dictionary containing the host's information and the command type.
        :return: message representing the current configuration.
        """
        self.check_config_json()
        dict_res = self.node.to_dict()
        return {"comm": Command.PING, "n": dict_res[1]}

    def reboot(self):
        """
        Reboots this node.
        """
        self.logger.info("Setting state to reboot ... Waiting for the next ping ...")
        time.sleep(3.0)
        self.logger.info("Rebooting system.")
        os.system("reboot")

    def update_hostname(self, new_hostname):
        """
        Updates the host with anew hostname.
        """
        old_hostname = self.node.name.replace(":", "--")
        new_hostname = new_hostname.replace(":", "--")

        if old_hostname != new_hostname:
            self.logger.info(
                "Updating current hostname from {} to {}.".format(
                    old_hostname, new_hostname
                )
            )

            with open("/etc/hostname", "w") as hostnameFile:
                hostnameFile.write(new_hostname)
                hostnameFile.close()
            os.system("hostname {}".format(new_hostname))
            self.node.name = new_hostname

    def update_ip_address(
        self, dhcp_manual, new_ip_address="", new_mask="", new_gateway=""
    ):
        """
        Updates the host with a new ip address
        """
        if self.node.ip_address != new_ip_address:
            if new_ip_address != "":
                self.logger.info(
                    "Updating current ip address from {} to {}, mask {}, default gateway {}.".format(
                        self.node.ip_address, new_ip_address, new_mask, new_gateway
                    )
                )
            else:
                self.logger.info(
                    "Updating current ip address from {} to DHCP.".format(
                        self.node.ip_address
                    )
                )
            self.change_ip_address(dhcp_manual, new_ip_address, new_mask, new_gateway)
            self.node.ip_address = self.get_ip_address()[0]

    def read_node_parameters(self):
        """
        Reads current node parameters, editing the name to include ':' where needed.
        """
        try:
            self.read_node_configuration()
        except IOError:
            self.logger.error("Configuration file not found. Adopting default values.")

        name = subprocess.check_output(["hostname"]).decode("utf-8").strip("\n")
        self.node.name = name.replace("--", ":")

    def read_node_configuration(self):
        """
        Reads the current node configuration from a binary file with the pickle module.
        """
        with open(self.configuration_file_path, "rb") as file:
            self.node = pickle.load(file)
            file.close()
            self.logger.info("Node configuration file read successfully.")

    def write_node_configuration(self):
        """
        Writes the current node configuration to a binary file with the pickle module. Overrides old files.
        """
        with open(self.configuration_file_path, "wb") as file:
            file.write(pickle.dumps(self.node))
            file.close()
            self.logger.info("Node configuration file updated successfully.")

    def get_ip_address(self):
        """
        Get the host's IP address with the 'ip addr' Linux command.
        :return: a tuple containing the host's ip address and network address.
        """
        command_out = subprocess.check_output(
            "ip addr show dev {} scope global".format(self.interface_name).split()
        ).decode("utf-8")

        lines = command_out.split("\n")
        address_line = lines[2].split()[1]

        return (
            ipaddress.IPv4Address(address_line[0 : address_line.index("/")]),
            ipaddress.IPv4Network(address_line, strict=False),
        )

    def change_ip_address(
        self, dhcp_manual, new_ip_address="", new_mask="", new_gateway=""
    ):
        """
        Execute the connmanclt tool to change the host' IP address.
        :param dchp_manual: either if its a DHCP ("dhcp") ou STATIC IP ("manual")
        :param new_ip_address: the new IP address. An ipaddress.IPv4Address object.
        :param net_address: new sub-network address. An ipaddress.IPv4Network object.
        :param default_gateway_address: the new default gateway
        :raise TypeError: new_ip_address or net_address are None or are neither ipaddress nor string objects.
        """
        service = self.get_connman_service_name()
        self.logger.debug(
            "Service for interface {} is {}.".format(self.interface_name, service)
        )

        if new_ip_address != "":
            self.logger.info(
                "Changing current IP address from {} to {}".format(
                    self.get_ip_address()[0], new_ip_address
                )
            )
            if new_gateway is None:
                new_gateway = Sector.get_default_gateway_of_address(new_ip_address)
        else:
            self.logger.info(
                "Changing current IP address from {} to DHCP".format(
                    self.get_ip_address()[0]
                )
            )

        subprocess.check_output(
            [
                "connmanctl config {} --ipv4 {} {} {} {}".format(
                    service, dhcp_manual, new_ip_address, new_mask, new_gateway
                )
            ],
            shell=True,
        )

        time.sleep(2)
        self.logger.debug(
            "IP address after update is {}".format(self.get_ip_address()[0])
        )

    def update_nameservers(self, nameserver_1="", nameserver_2=""):
        service = self.get_connman_service_name()
        self.logger.info(
            "Changing DSN server to {} and {}".format(nameserver_1, nameserver_2)
        )
        subprocess.check_output(
            [
                "connmanctl config {} --nameservers {} {}".format(
                    service, nameserver_1, nameserver_2
                )
            ],
            shell=True,
        )

    def get_connman_service_name(self):
        """
        Returns the service name assigned to manage an interface.
        @fixme: services with spaces on their names won't be detected!
        :return: A service's name.
        :raise ValueError: service is not found.
        """
        services = subprocess.check_output(
            ["connmanctl services"], stderr=subprocess.STDOUT, shell=True
        ).decode("utf-8")

        for service in services.split():

            if service.startswith("ethernet_"):
                service_properties = subprocess.check_output(
                    ["connmanctl services " + service],
                    stderr=subprocess.STDOUT,
                    shell=True,
                ).decode("utf-8")

                for prop in service_properties.split("\n"):
                    if prop.strip().startswith("Ethernet"):
                        data = prop.split("[")[1].strip()[:-1].split(",")
                        for d_info in data:
                            d_info = d_info.strip()
                            if d_info.startswith("Interface"):
                                if d_info == "Interface={}".format(self.interface_name):
                                    return service

        raise ValueError(
            "Connmanctl service could not be found for interface {}".format(
                self.interface_name
            )
        )


class Command:
    """
    A simple class to wrap command codes.
    """

    (
        PING,
        REBOOT,
        EXIT,
        END,
        TYPE,
        APPEND_TYPE,
        REMOVE_TYPE,
        NODE,
        APPEND_NODE,
        REMOVE_NODE,
        SWITCH,
        GET_TYPES,
        GET_UNREG_NODES_SECTOR,
        GET_REG_NODES_SECTOR,
        GET_REG_NODE_BY_IP,
        OK,
        FAILURE,
        SET_IP,
        SET_HOSTNAME,
        SET_NAMESERVERS,
    ) = range(20)

    @staticmethod
    def command_name(command):
        """
        Returns the name of a command.
        :param command: a command id.
        :return: a given command's name.
        """
        for key in Command.__dict__.keys():
            if Command.__dict__[key] == command:
                return key

    @staticmethod
    def is_loggable(command):
        """
        Checks if a given command should appear in logs.
        :param command: a command id.
        :return: True if command should be appear in logs and False, otherwise.
        """
        return command not in [
            Command.GET_TYPES,
            Command.GET_UNREG_NODES_SECTOR,
            Command.GET_REG_NODES_SECTOR,
            Command.GET_REG_NODE_BY_IP,
            Command.OK,
            Command.FAILURE,
            Command.SET_IP,
            Command.SET_HOSTNAME,
            Command.SET_NAMESERVERS,
        ]


class SectorNotFoundError(Exception):
    """
    A simple exception class to represent sector errors.
    """

    pass


class Sector:
    """
    A static class providing helper functions to manage sectors.
    """

    SECTORS = [("Sala" + str(i).zfill(2)) for i in range(1, 21)] + [
        "Conectividade",
        "LINAC",
        "RF",
        "Fontes",
        "Outros",
    ]

    SUBNETS = (
        [
            [
                ipaddress.ip_network(u"10.128.1.0/24"),
                ipaddress.ip_network(u"10.128.255.0/24"),
            ]
        ]
        + [ipaddress.ip_network(u"10.128.{}.0/24".format(i)) for i in range(101, 124)]
        + [ipaddress.ip_network(u"10.128.{}.0/24".format(i)) for i in range(201, 222)]
        + [ipaddress.ip_network(u"10.128.{}.0/24".format(i)) for i in range(150, 153)]
    )

    # SECTORS_LIST = []
    SECTORS_DICT = {}
    for i in range(1, 22):
        SECTORS_DICT[
            str(ipaddress.ip_network(u"10.128.{}.0/24".format(i + 100)))
        ] = "CON-RACK{}".format(str(i).zfill(2))

    @staticmethod
    def subnets():
        return Sector.SUBNETS

    @staticmethod
    def get_sectors_dict():
        return Sector.SECTORS_DICT

    @staticmethod
    def sectors():
        return Sector.SECTORS

    @staticmethod
    def get_sector_by_ip_address(ip_address=None):
        """
        Returns the sector of a node based on its IP address.
        :param ip_address: the IP address of a host.
        :return: the sector that contains the given IP address.
        :raise SectorNotFoundError: IP address is not contained in any sub-network.
        """
        for idx, subnet in enumerate(Sector.SUBNETS):
            if type(subnet) is list:
                for s in subnet:
                    if ip_address in s.hosts():
                        return Sector.SECTORS[idx]
            elif ip_address in subnet.hosts():
                return Sector.SECTORS[idx]

        return Sector.SECTORS[-1]

    @staticmethod
    def get_default_gateway_of_address(ip_address=None):
        """
        Returns the default gateway of a node based on its IP address.
        :param ip_address: the IP address of a host.
        :return: the default gateway of that host. An ipaddress.IPv4Address object.
        :raise SectorNotFoundError: IP address is not contained in any sub-network.
        """
        for subnet in Sector.SUBNETS:
            if type(subnet) is list:
                for s in subnet:
                    if ip_address in s.hosts():
                        return s.network_address + 1
            elif ip_address in subnet.hosts():
                return subnet.network_address + 1

        return Sector.SUBNETS[-1].network_address + 1

    @staticmethod
    def get_network_address_from_ip_address(ip_address):
        ip_interface = ipaddress.ip_interface(ip_address)
        return ipaddress.ip_network(ip_interface, strict=False)


class NodeState:
    """
    Valid states for any host in the Controls Group network.
    """

    DISCONNECTED, MIS_CONFIGURED, CONNECTED, REBOOTING = range(4)

    @staticmethod
    def to_string(state):
        """
        :param state: the state to be converted to string.
        :return: string representation of a state.
        """

        if state == NodeState.DISCONNECTED:
            return "Disconnected"

        elif state == NodeState.CONNECTED:
            return "Connected"

        elif state == NodeState.MIS_CONFIGURED:
            return "Mis-configured"

        elif state == NodeState.REBOOTING:
            return "Rebooting"

        return "Unknown state"


class Type:
    """
    This class provides a wrapper for host types.
    """

    KEY_PREFIX = "Type:"
    KEY_PREFIX_LEN = len(KEY_PREFIX)

    NUM_TYPES = 8
    (
        UNDEFINED,
        POWER_SUPPLY,
        COUNTING_PRU,
        SERIAL_THERMO,
        MBTEMP,
        AGILENT4UHV,
        MKS937B,
        SPIXCONV,
    ) = range(NUM_TYPES)
    TYPES = []

    @staticmethod
    def from_code(type_code):
        if type_code not in range(Type.NUM_TYPES):
            raise ValueError("type_code {} invalid.".format(type_code))

        return Type(code=type_code)

    def __init__(self, **kwargs):
        """
        Initializes a type instance.
        :param name: a type's name.
        :param description: A brief description of the type
        :param sha: A way to provide error detection.
        """
        self.code = kwargs.get("code", Type.UNDEFINED)

    @property
    def description(self):
        if self.code == Type.POWER_SUPPLY:
            return "Desc: Power Supply"
        elif self.code == Type.COUNTING_PRU:
            return "Desc: CountingPRU"
        elif self.code == Type.SERIAL_THERMO:
            return "Desc: Thermo Probe"
        elif self.code == Type.MBTEMP:
            return "Desc: MBTemp"
        elif self.code == Type.AGILENT4UHV:
            return "Desc: Agilent 4UHV"
        elif self.code == Type.MKS937B:
            return "Desc: MKS 937b"
        elif self.code == Type.SPIXCONV:
            return "Desc: SPIxCONV"
        else:
            return "Desc: Undefined"

    @property
    def name(self):

        if self.code == Type.POWER_SUPPLY:
            return "Power Supply"
        elif self.code == Type.COUNTING_PRU:
            return "CountingPRU"
        elif self.code == Type.SERIAL_THERMO:
            return "Thermo Probe"
        elif self.code == Type.MBTEMP:
            return "MBTemp"
        elif self.code == Type.AGILENT4UHV:
            return "Agilent 4UHV"
        elif self.code == Type.MKS937B:
            return "MKS 937b"
        elif self.code == Type.SPIXCONV:
            return "SPIxCONV"
        else:
            return "Undefined"

    @name.setter
    def name(self, value):
        pass

    @description.setter
    def description(self, value):
        pass

    def __eq__(self, other):
        """
        A way to compare two types.
        :param other: other type instance.
        :return: True if the code is equal.
        """
        if other is None:
            return False

        return other.code == self.code

    def __str__(self):
        return "{}\t{}".format(type(self), str(self.__dict__))

    def to_dict(self):
        return {"name": self.name, "description": self.description}

    @staticmethod
    def get_types():
        d = {}
        for _t in Type.TYPES:
            d[_t.code] = _t.to_dict()
        return d


for n in range(Type.NUM_TYPES):
    Type.TYPES.append(Type(code=n))


class Node:
    """
    This class represents a Controls group's host. Each host has a symbolic name, a valid IP address, a type
    and the sector where it is located.
    """

    KEY_PREFIX = "Node:"

    def __init__(self, **kwargs):
        """
        Initializes a node instance.
        :param name: a node's name.
        :param ip: string representation of a node's ip address.
        :param state: current node's state.
        :param type_node: current node's type.
        :param sector: current node's sector.
        :param counter: heart beat count.
        :param details: details provided by the host
        :param config_time: when the host found it's configuration
        """

        self.name = kwargs.get("name", "r0n0")
        self.ip_address = kwargs.get("ip_address", "10.128.0.0")
        self.state = kwargs.get("state", NodeState.CONNECTED)
        self.state_string = NodeState.to_string(self.state)
        self.type = kwargs.get("type_node", Type(code=Type.UNDEFINED))
        self.sector = kwargs.get("sector", 1)
        self.counter = kwargs.get("counter", 0)

        self.details = kwargs.get("details", "")
        self.config_time = kwargs.get("config_time", "")

    def to_dict(self):
        """
        Returns a node's dictionary representation.
        :return: node's key with prefix, the node's dictionary representation and the type of the node.
        """
        node_dict = copy.deepcopy(self.__dict__)
        if node_dict["type"] is not None:
            node_dict["type"] = self.type.code
        else:
            node_dict["type"] = Type(code=Type.UNDEFINED)
        return self.get_key(), node_dict

    def from_dict(self, node_dict, **kwargs):
        """
        Load the values from a redis set.
        :param node_dict: dictionary representing the node object according to the pattern defined
        in the method get_set() from the Node object.
        :raise TypeError: the dictionary provided is None.
        """
        for key in node_dict:
            if key == "type":
                _type = node_dict[key]
                if _type is not None:
                    if type(_type) != Type:
                        node_dict[key] = Type(code=int(_type))
                    else:
                        node_dict[key] = _type
                else:
                    node_dict[key] = Type(code=Type.UNDEFINED)

            setattr(self, key, node_dict[key])

    def get_key(self):
        """
        :return: returns the node's key with prefix
        """
        return (Node.KEY_PREFIX + str(self.ip_address)).replace(" ", "")
