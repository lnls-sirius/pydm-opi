import threading
import redis
import time
import subprocess
import logging

import os
import sys

if len(sys.argv) == 1:
    sys.path.insert(0, "/root/bbb-function/src/scripts")
    from bbb import BBB

SERVER_IP = "10.128.255.3"
CONFIG_PATH = "/var/tmp/bbb.bin"
LOG_PATH_SERVER = "/var/tmp/bbbread_server.log"
LOG_PATH_BBB = "/var/tmp/bbbread.log"


def update_local_db():
    """Updates local redis database with device.json info"""
    node = BBB(CONFIG_PATH)
    local_db = redis.StrictRedis(host="127.0.0.1", port=6379, socket_timeout=2)
    info = node.get_current_config()["n"]

    info["ping_time"] = str(time.time())
    services = subprocess.check_output(["connmanctl", "services"]).decode().split("\n")

    """
    ip_specs is a string similar to:
    '... IPv4 = [ Method=XXXXX, Address=W.X.Y.Z  ...
    ... IPv4.Configuration ...
    ... Nameservers = [ X.X.X.X, Y.Y.Y.Y ] 
    Nameservers.Configuration ...'
    """

    for service in services:
        if "*AO Wired" in service or "*AR Wired" in service:
            service = service.split(16 * " ")[1]
            ip_specs = subprocess.check_output(
                ["connmanctl", "services", service]
            ).decode()
            # Determines IP type
            if "IPv4.Configuration = [ Method=dhcp" in ip_specs:
                info["ip_type"] = "DHCP"
            else:
                info["ip_type"] = "StaticIP"
            info["nameservers"] = ip_specs.split("Nameservers")[1][5:-5]
            # Determines IP
            ip_string = ip_specs.split("IPv4")[1].split(",")[1][9:]
            if "10.128.1" in ip_string:
                info["sector"] = ip_string.split(".")[2][1:]
            else:
                info["sector"] = "1"
            break
        else:
            info["ip_type"] = "Undefined"
            info["nameservers"] = "Undefined"
            info["sector"] = "1"

    local_db.hmset("device", info)
    return info["ip_address"], info["name"]


class Command:
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


class RedisServer:
    """Runs on Control System's Server"""

    def __init__(self, host=SERVER_IP, log_path=LOG_PATH_SERVER):
        # Configuring redis server
        self.local_db = redis.Redis(host=host)

        # Configuring logging
        self.logger = logging.getLogger("bbbreadServer")
        self.logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter("%(levelname)s:%(asctime)s:%(name)s:%(message)s")
        try:
            file_handler = logging.FileHandler(log_path)
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)
        except:
            self.logger.exception(
                "Failed to create file_handler at '{}'".format(log_path)
            )
            pass

    # TODO: Change function name
    def list_connected(self, ip="", hostname=""):
        """Returns a list of all BeagleBone Blacks connected to REDIS database
        If IP or hostname is specified lists only the ones with the exact specified parameter"""
        if ip and hostname:
            all_instances = self.local_db.keys("BBB:{}:{}".format(ip, hostname))
            command_instances = []
        elif ip and not hostname:
            all_instances = self.local_db.keys("BBB:{}:*".format(ip))
            command_instances = self.local_db.keys("BBB:{}:*:Command".format(ip))
        elif not ip and hostname:
            all_instances = self.local_db.keys("BBB:*:{}".format(hostname))
            command_instances = []
        else:
            all_instances = self.local_db.keys("BBB:*")
            command_instances = self.local_db.keys("BBB:*:Command")
        all_connected = []
        for node in all_instances:
            if node in command_instances:
                continue
            all_connected.append(node.decode())
        return all_connected

    def get_node(self, hashname):
        """Returns a BBB info, if an error occurs returns False"""
        try:
            info = self.local_db.hgetall(hashname)
            return info
        except Exception as e:
            self.logger.error("Failed to return nodes info due to error:\n{}".format(e))
            return False

    def send_command(self, ip: str, command, hostname=""):
        """Sends a command to a BeagleBone Black
        Returns False if it fails to send command"""
        try:
            bbb_hashname = self.list_connected(ip, hostname)
            if len(bbb_hashname) == 1:
                bbb_state = self.local_db.hget(bbb_hashname[0], "state_string").decode()
                if bbb_state != "Connected":
                    self.logger.error("failed to send command, node is inactive")
                    return False
                bbb_command_listname = "{}:Command".format(bbb_hashname[0])
                check = self.local_db.rpush(bbb_command_listname, command)
                return bool(check)
            elif len(bbb_hashname) < 1:
                self.logger.error(
                    "no node found with the specified IP and hostname:" + ip + hostname
                )
            else:
                self.logger.error(
                    "two or more nodes found with the specified ip, please specify a hostname"
                )
            return False
        except Exception as e:
            self.logger.critical(
                "A fatal error occurred while sending the command:\n{}".format(e)
            )
            return False

    # TODO: verify if this method is still necessary
    def generate_hashname(self, bbb_ip: str):
        """Verifies if there is one hash for the specified IP.
        Returns the BBB hash name or NONE"""
        bbb_hashname = sorted(self.local_db.keys("BBB:{}:*".format(bbb_ip)))
        bbb_commandlistname = self.local_db.keys("BBB:{}:*:Command".format(bbb_ip))
        if len(bbb_hashname) == 1:
            return bbb_hashname[0].decode()
        elif len(bbb_hashname) == 2 and bbb_commandlistname:
            return bbb_hashname[0].decode()
        elif len(bbb_hashname) < 1:
            self.logger.error(
                "Failed to find any BBB redis instance for the specified IP"
            )
            return None
        else:
            self.logger.error("Two or more hash with the same IP")
            return None

    def bbb_state(self, hashname: str):
        """Verifies if node is active. Ping time inferior to 15 seconds
        Zero if active node, One if disconnected and Two if moved to other hash"""
        last_ping = float(self.local_db.hget(hashname, "ping_time").decode())
        time_since_ping = time.time() - last_ping
        node_state = self.local_db.hget(hashname, "state_string").decode()
        if node_state[:3] == "BBB":
            return 2
        elif time_since_ping >= 11:
            self.local_db.hset(hashname, "state_string", "Disconnected")
            return 1
        return 0

    # TODO: verify if this method is still necessary
    def move_bbb(self, hashname: str):
        """Verifies if a node was successfully moved to another hash.
        If so, deletes it's previous hashname"""
        if self.local_db.exists(hashname):
            new_hash = self.local_db.hget(hashname, "state_string").decode()
            if new_hash == "BBB:IP-moved-to-DHCP":
                hashes = self.list_connected(hostname=hashname.split(":")[2])
                if len(hashes) == 2:
                    self.local_db.delete(hashname)
                    return True
                return False
            elif new_hash[:3] == "BBB":
                if (
                    self.local_db.exists(new_hash)
                    and self.local_db.hget(new_hash, "state_string") == b"Connected"
                ):
                    self.local_db.delete(hashname)
                    return True
            else:
                self.logger.warning("BBB didn't change IP")
                return False
        else:
            self.logger.warning("Invalid hashname")
            return False

    def delete_bbb(self, hashname: str):
        """Removes a hash from redis database"""
        self.local_db.delete(hashname)

    def change_hostname(self, ip: str, new_hostname: str, current_hostname=""):
        """Changes a BeagleBone Black hostname
        Returns false if an error occurs while sending the command or BBB isn't connected to Redis"""
        command = "{};{}".format(Command.SET_HOSTNAME, new_hostname)
        check = self.send_command(ip, command, current_hostname)
        # If command is sent successfully logs hostname change
        if check:
            self.logger.info("{} NEW HOSTNAME - {}".format(ip, new_hostname))
        return check

    def change_nameservers(
        self, ip: str, nameserver_1: str, nameserver_2: str, hostname=""
    ):
        """Changes a BeagleBone Black nameservers
        Returns false if an error occurs while sending the command or BBB isn't connected to Redis"""
        command = "{};{};{}".format(Command.SET_NAMESERVERS, nameserver_1, nameserver_2)
        check = self.send_command(ip, command, hostname)
        # If command is sent successfully logs hostname change
        if check:
            self.logger.debug(
                "{} NEW NAMESERVERS - {}  {}".format(ip, nameserver_1, nameserver_2)
            )
        return check

    def change_ip(
        self,
        current_ip: str,
        ip_type: str,
        hostname="",
        new_ip="",
        new_mask="",
        new_gateway="",
    ):
        """Changes a BeagleBone Black IP address (DHCP or manual)
        Returns false if an error occurs while sending the command or BBB isn't connected to Redis"""
        command = "{};{}".format(Command.SET_IP, ip_type)
        if ip_type == "manual":
            # Verifies if new_ip is possible
            check_integrity = new_ip.split(".")
            if len(check_integrity) != 4:
                self.logger.warning("{} NEW IP NOT FORMATTED CORRECTLY")
                return False
            # Verifies if specified IP is available
            ip_available = os.system('ping "-c" 1 -w2 "10.0.6.6" > /dev/null 2>&1')
            if ip_available:
                command += ";{};{};{}".format(new_ip, new_mask, new_gateway)
            else:
                self.logger.warning("{} IP NOT AVAILABLE")
                return False
        check = self.send_command(current_ip, command, hostname)
        if check:
            self.logger.info(
                "{} NEW IP - type:{} - new ip: {} - mask: {} - gateway: {}".format(
                    current_ip, ip_type, new_ip, new_mask, new_gateway
                )
            )
        return check

    def reboot_node(self, ip: str, hostname=""):
        """Reboots the specified BeagleBone Black
        Returns false if an error occurs while sending the command or BBB isn't connected to Redis"""
        check = self.send_command(ip, Command.REBOOT, hostname)
        if check:
            self.logger.info("{} REBOOT".format(ip))
        return check


# TODO: Implement commutable server IP
class RedisClient:
    """
    A class to write BBB information on a REDIS server
    """

    def __init__(self, path=CONFIG_PATH, remote_host=SERVER_IP, log_path=LOG_PATH_BBB):
        self.bbb = BBB(path)
        # Configuring logging
        self.logger = logging.getLogger("bbbread")
        self.logger.setLevel(logging.INFO)
        formatter = logging.Formatter("%(levelname)s:%(asctime)s:%(name)s:%(message)s")
        try:
            file_handler = logging.FileHandler(log_path)
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)
        except:
            self.logger.exception(
                "Failed to crate file_handler at '{}'".format(file_handler)
            )

        # Defining local and remote database
        self.remote_host = remote_host
        self.local_db = redis.Redis(host="127.0.0.1", port=6379, socket_timeout=2)
        self.remote_db = redis.Redis(host=self.remote_host, port=6379, socket_timeout=2)

        # Formats remote hash name as "BBB:IP_ADDRESS:HOSTNAME"
        update_local_db()
        self.bbb_ip, self.bbb_hostname = self.local_db.hmget(
            "device", "ip_address", "name"
        )
        self.bbb_ip = self.bbb_ip.decode()
        self.bbb_hostname = self.bbb_hostname.decode()
        self.hashname = "BBB:{}:{}".format(self.bbb_ip, self.bbb_hostname)
        self.command_listname = "BBB:{}:{}:Command".format(
            self.bbb_ip, self.bbb_hostname
        )
        self.remote_db.rpush(self.command_listname, "")

        # Pinging thread
        self.ping_thread = threading.Thread(target=self.ping_remote, daemon=True)
        self.pinging = True
        self.ping_thread.start()

        # Listening thread
        self.listen_thread = threading.Thread(target=self.listen, daemon=True)
        self.listening = True
        self.listen_thread.start()

    def ping_remote(self):
        """Thread that updates remote database every 10s, if pinging is enabled"""
        while True:
            if not self.pinging:
                time.sleep(2)
                continue
            # self.remote_db = redis.Redis(host=self.remote_host, port=6379)
            try:
                self.force_update()
                self.logger.debug("Remote DataBase pinged successfully")
                time.sleep(10)
            except Exception as e:
                self.logger.error("Pinging Thread died:\n{}".format(e))
                time.sleep(1)

    def listen(self):
        """Thread to process server's commands"""
        while True:
            time.sleep(2)
            if not self.listening:
                time.sleep(2)
                continue
            try:
                self.command_listname = self.hashname + ":Command"
                if self.remote_db.keys(self.command_listname):
                    command = self.remote_db.lpop(self.command_listname).decode()
                    command = command.split(";")
                    # Verifies if command is an integer
                    try:
                        command[0] = int(command[0])
                    except ValueError:
                        self.logger.error(
                            "Failed to convert first part of the command to integer"
                        )
                        continue
                    self.logger.info("command received {}".format(command))
                    if command[0] == Command.REBOOT:
                        self.logger.info("Reboot command received")
                        self.bbb.reboot()

                    # TODO: Needs to lock update_local_db in order to prevent state_string to be quoted wrong
                    elif command[0] == Command.SET_HOSTNAME and len(command) == 2:
                        new_hostname = command[1]
                        # bbb_ip = self.local_db.hget('device', 'ip_address').decode()
                        # self.remote_db.hset(self.hashname, 'state_string', 'BBB:{}:{}'.format(bbb_ip, new_hostname))
                        self.bbb.update_hostname(new_hostname)
                        # Updates variable names
                        self.logger.info("renaming command")
                        # self.remote_db = redis.StrictRedis(host=self.remote_host, port=6379, socket_timeout=2)
                        # if self.remote_db.keys(self.command_listname):
                        #     self.remote_db.rename(self.command_listname, self.hashname + ":Command")
                        self.logger.info("Hostname changed to " + new_hostname)

                    elif command[0] == Command.SET_IP:
                        ip_type = command[1]
                        # Verifies if IP is to be set manually
                        if ip_type == "manual" and len(command) == 5:
                            new_ip = command[2]
                            new_mask = command[3]
                            new_gateway = command[4]
                            # bbb_hostname = self.local_db.hget('device', 'name').decode()
                            # self.remote_db.hset(self.hashname, 'state_string', 'BBB:{}:{}'.format(new_ip,
                            #                                                                          bbb_hostname))
                            self.bbb.update_ip_address(
                                ip_type, new_ip, new_mask, new_gateway
                            )
                            # Updates variable names
                            self.logger.info("UPDATING")
                            self.logger.info("renaming command")
                            # self.remote_db = redis.StrictRedis(host=self.remote_host, port=6379, socket_timeout=2)
                            # if self.remote_db.keys(self.command_listname):
                            #     self.remote_db.rename(self.command_listname, self.hashname + ":Command")
                            self.logger.info(
                                "IP manually changed to {}, netmask {}, gateway {}".format(
                                    new_ip, new_mask, new_gateway
                                )
                            )

                        # Verifies if IP is DHCP
                        elif ip_type == "dhcp":
                            # self.remote_db.hset(self.hashname, 'state_string', 'BBB:IP-moved-to-DHCP')
                            self.bbb.update_ip_address(ip_type)
                            # Updates variable names
                            time.sleep(1)
                            self.logger.info("renaming command")
                            # self.remote_db = redis.StrictRedis(host=self.remote_host, port=6379, socket_timeout=2)
                            # if self.remote_db.keys(self.command_listname):
                            #     self.remote_db.rename(self.command_listname, self.hashname + ":Command")
                            self.logger.info("IP changed to DHCP")

                    elif command[0] == Command.SET_NAMESERVERS and len(command) == 3:
                        nameserver_1 = command[1]
                        nameserver_2 = command[2]
                        self.bbb.update_nameservers(nameserver_1, nameserver_2)
                        self.logger.info("Nameservers changed")
            except Exception as e:
                self.logger.error("Listening Thread died:\n{}".format(e))
                time.sleep(1)
                self.remote_db = redis.StrictRedis(
                    host=self.remote_host, port=6379, socket_timeout=2
                )
                continue

    def force_update(self, log=False):
        """Updates local and remote database"""
        if log:
            self.logger.info("updating local db")
        new_ip, new_hostname = update_local_db()
        if log:
            self.logger.info("local db updated")
        info = self.local_db.hgetall("device")
        # Formats remote hash name as "BBB:IP_ADDRESS"
        self.hashname = "BBB:{}:{}".format(new_ip, new_hostname)
        if new_ip != self.bbb_ip or new_hostname != self.bbb_hostname:
            old_hashname = "BBB:{}:{}".format(self.bbb_ip, self.bbb_hostname)
            old_info = info.copy()
            old_info[b"state_string"] = self.hashname
            old_info[b"name"] = self.bbb_hostname
            old_info[b"ip_address"] = self.bbb_ip
            if self.remote_db.keys(old_hashname + ":Command"):
                self.remote_db.rename(
                    old_hashname + ":Command", self.hashname + ":Command"
                )
            self.logger.info(
                "old ip: {}, new ip: {}, old hostname: {}, new hostname: {}".format(
                    self.bbb_ip, new_ip, self.bbb_hostname, new_hostname
                )
            )
            self.remote_db.hmset(old_hashname, old_info)
        # Updates remote hash
        if log:
            self.logger.info("updating remote db")
        self.remote_db.hmset(self.hashname, info)
        self.bbb_ip, self.bbb_hostname = (new_ip, new_hostname)


if __name__ == "__main__":
    server = RedisServer()
    client = RedisClient()
    sys.exit()
