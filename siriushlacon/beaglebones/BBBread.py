import threading
import redis
import time
import subprocess
import logging
from logging.handlers import RotatingFileHandler

import os
import sys

LA_SERVER_IP = "10.0.38.46"
CA_SERVER_IP = "10.0.38.59"
CONFIG_PATH = "/var/tmp/bbb.bin"
LOG_PATH_SERVER = "bbbread.log"
LOG_PATH_BBB = "/var/log/bbbread.log"

# Verifies if device is a BBB
if "armv7" in subprocess.check_output(["uname", "-a"]).decode():
    device = "bbb"
    sys.path.insert(0, "/root/bbb-function/src/scripts")
    from bbb import BBB

    node = BBB(CONFIG_PATH)
else:
    device = "server"


def update_local_db():
    """Updates local redis database with device.json info"""

    local_db = redis.StrictRedis(host="127.0.0.1", port=6379, socket_timeout=2)
    info = node.get_current_config()["n"]
    info["ping_time"] = str(time.time())

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
        RESTART_SERVICE,
        STOP_SERVICE,
    ) = range(22)


class RedisServer:
    """Runs on Control System's Server"""

    def __init__(self, log_path=LOG_PATH_SERVER):
        # Configuring logging
        self.logger = logging.getLogger("bbbreadServer")
        self.logger.setLevel(logging.DEBUG)
        self.logger.debug("Starting up BBBread Server")

        # Probably connecting to a existing server, tries to connect to primary server
        self.local_db = redis.StrictRedis(
            host=LA_SERVER_IP, port=6379, socket_timeout=2
        )
        try:
            self.local_db.ping()
            self.logger.debug("Connected to LA-RaCtrl-CO-Srv-1 Redis Server")
        # If primary server is not available, tries to connect to backup server
        except redis.exceptions.ConnectionError:
            self.local_db = redis.StrictRedis(
                host=CA_SERVER_IP, port=6379, socket_timeout=2
            )
            try:
                self.local_db.ping()
                self.logger.debug("Connected to CA-RaCtrl-CO-Srv-1 Redis Server")
            # Case no BBBread server is found
            except redis.exceptions.ConnectionError:
                self.logger.error("No BBBread Server found")
                raise Exception("No BBBread Server found")

    def get_logs(self, hashname=None):

        if hashname:
            return [
                [key.decode("utf-8"), value.decode("utf-8")]
                for key, value in self.local_db.hgetall(hashname).items()
            ]
        else:
            return [name.decode("utf-8") for name in self.local_db.keys("BBB:*:Logs")]

    # TODO: Change function name
    def list_connected(self, ip="", hostname=""):
        """Returns a list of all BeagleBone Blacks connected to REDIS database
        If IP or hostname is specified lists only the ones with the exact specified parameter"""
        command_instances = []
        log_instances = []
        all_connected = []

        if ip and hostname:
            all_instances = self.local_db.keys("BBB:{}:{}".format(ip, hostname))
        elif ip and not hostname:
            all_instances = self.local_db.keys("BBB:{}:*".format(ip))
            command_instances = self.local_db.keys("BBB:{}:*:Command".format(ip))
            log_instances = self.local_db.keys("BBB:{}:*:Logs".format(ip))
        elif not ip and hostname:
            all_instances = self.local_db.keys("BBB:*:{}".format(hostname))
        else:
            all_instances = self.local_db.keys("BBB:*")
            command_instances = self.local_db.keys("BBB:*:Command")
            log_instances = self.local_db.keys("BBB:*:Logs")

        for node in all_instances:
            if node in command_instances or node in log_instances:
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

    def send_command(self, ip: str, command, hostname="", override=False):
        """Sends a command to a BeagleBone Black
        Returns False if it fails to send command"""
        try:
            bbb_hashname = self.list_connected(ip, hostname)

            if override and hostname:
                bbb_hashname = ["BBB:{}:{}".format(ip, hostname)]
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
            self.logger.error(
                "A fatal error occurred while sending the command:\n{}".format(e)
            )
            return False

    def bbb_state(self, hashname: str):
        """Verifies if node is active. Ping time inferior to 15 seconds
        Zero if active node, One if disconnected and Two if moved to other hash"""
        now = time.time()

        last_ping = float(self.local_db.hget(hashname, "ping_time").decode())
        time_since_ping = now - last_ping
        node_state = self.local_db.hget(hashname, "state_string").decode()
        last_logs = self.local_db.hvals(hashname + ":Logs")
        if node_state[:3] == "BBB":
            return 2
        elif time_since_ping >= 25:
            if node_state != "Disconnected":
                self.local_db.hset(hashname, "state_string", "Disconnected")
                self.log_remote(hashname + ":Logs", "Disconnected", int(now) - 10800)
            return 1
        if last_logs:
            known_status = last_logs[-1].decode()
            if known_status == "Disconnected" or known_status == hashname:
                self.log_remote(hashname + ":Logs", "Reconnected", int(now) - 10800)
        return 0

    def delete_bbb(self, hashname: str):
        """Removes a hash from redis database"""
        self.local_db.delete(hashname)

    def change_hostname(
        self, ip: str, new_hostname: str, current_hostname="", override=False
    ):
        """Changes a BeagleBone Black hostname
        Returns false if an error occurs while sending the command or BBB isn't connected to Redis"""
        command = "{};{}".format(Command.SET_HOSTNAME, new_hostname)
        check = self.send_command(ip, command, current_hostname, override)
        # If command is sent successfully logs hostname change
        if check:
            self.logger.info("{} NEW HOSTNAME - {}".format(ip, new_hostname))
        return check

    def change_nameservers(
        self, ip: str, nameserver_1: str, nameserver_2: str, hostname="", override=False
    ):
        """Changes a BeagleBone Black nameservers
        Returns false if an error occurs while sending the command or BBB isn't connected to Redis"""
        command = "{};{};{}".format(Command.SET_NAMESERVERS, nameserver_1, nameserver_2)
        check = self.send_command(ip, command, hostname, override)
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
        override=False,
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
        check = self.send_command(current_ip, command, hostname, override)
        if check:
            self.logger.info(
                "{} NEW IP - type:{} - new ip: {} - mask: {} - gateway: {}".format(
                    current_ip, ip_type, new_ip, new_mask, new_gateway
                )
            )
        return check

    def reboot_node(self, ip: str, hostname="", override=False):
        """Reboots the specified BeagleBone Black
        Returns false if an error occurs while sending the command or BBB isn't connected to Redis"""
        check = self.send_command(ip, Command.REBOOT, hostname, override)
        if check:
            self.logger.info("{} REBOOT".format(ip))
        return check

    def stop_service(self, ip: str, service: str, hostname="", override=False):
        """Stops the specified service on the given BBB"""
        command = "{};{}".format(Command.STOP_SERVICE, service)
        check = self.send_command(ip, command, hostname, override)
        if check:
            self.logger.info("{} SERVICE STOPPED - {}".format(ip, service))
        return check

    def restart_service(self, ip: str, service: str, hostname="", override=False):
        """Restarts the specified service on the given BBB"""
        command = "{};{}".format(Command.RESTART_SERVICE, service)
        check = self.send_command(ip, command, hostname, override)
        if check:
            self.logger.info("{} SERVICE RESTARTED - {}".format(ip, service))
        return check

    def log_remote(self, bbb, message, date):
        self.local_db.hset(bbb, date, message)


# TODO: Implement commutable server IP
class RedisClient:
    """
    A class to write BBB information on a REDIS server
    """

    def __init__(
        self,
        path=CONFIG_PATH,
        remote_host_1=LA_SERVER_IP,
        remote_host_2=CA_SERVER_IP,
        log_path=LOG_PATH_BBB,
    ):
        # Configuring logging
        self.logger = logging.getLogger("bbbread")
        self.logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter("%(levelname)s:%(asctime)s:%(name)s:%(message)s")
        file_handler = RotatingFileHandler(log_path, maxBytes=15000000, backupCount=5)
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

        self.logger.debug("Starting BBBread up")

        # Defining local and remote database
        self.local_db = redis.StrictRedis(host="127.0.0.1", port=6379, socket_timeout=4)
        self.remote_db_1 = redis.StrictRedis(
            host=remote_host_1, port=6379, socket_timeout=4
        )
        self.remote_db_2 = redis.StrictRedis(
            host=remote_host_2, port=6379, socket_timeout=4
        )
        self.server_connected = False

        self.logger.debug("Searching for active database")
        self.remote_db = self.find_active()

        # Defining BBB object and formatting remote hash name as "BBB:IP_ADDRESS:HOSTNAME"
        self.bbb = BBB(path)
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

        # Pinging thread
        self.ping_thread = threading.Thread(target=self.ping_remote, daemon=True)
        self.pinging = True
        self.ping_thread.start()
        self.logger.debug("Pinging thread started")

        # Listening thread
        self.listen_thread = threading.Thread(target=self.listen, daemon=True)
        self.listening = True
        self.listen_thread.start()
        self.logger.debug("Listening thread started")
        self.logger.debug("BBBread startup completed")
        self.logs_name = "BBB:{}:{}:Logs".format(self.bbb_ip, self.bbb_hostname)

    def find_active(self):
        while True:
            try:
                self.remote_db_1.ping()
                self.logger.debug("Connected to LA-RaCtrl-CO-Srv-1 Redis Server")
                self.server_connected = True
                return self.remote_db_1
            except redis.exceptions.ConnectionError:
                try:
                    self.remote_db_2.ping()
                    self.logger.debug("Connected to CA-RaCtrl-CO-Srv-1 Redis Server")
                    self.server_connected = True
                    return self.remote_db_2
                except redis.exceptions.ConnectionError:
                    self.logger.critical("No remote database found")
                    raise Exception("No remote database found")
            self.logger.info("Server not found. Retrying to connect in 10 seconds...")
            time.sleep(10)

    def ping_remote(self):
        """Thread that updates remote database every 10s, if pinging is enabled"""
        while True:
            if not self.pinging or not self.server_connected:
                time.sleep(2)
                continue
            try:
                self.force_update()
                time.sleep(10)
            except Exception as e:
                now = int(time.time()) - 10800
                self.logger.error("Pinging Thread died:\n{}".format(e))
                self.log_remote("Pinging Thread died: {}".format(e), now)
                time.sleep(1)
                self.find_active()

    def listen(self):
        """Thread to process server's commands"""
        while True:
            time.sleep(2)
            if not self.listening:
                time.sleep(2)
                continue

            time.sleep(1)
            now = int(time.time()) - 10800
            self.command_listname = self.hashname + ":Command"
            command = []

            try:
                if self.remote_db.keys(self.command_listname):
                    command = self.remote_db.lpop(self.command_listname).decode()
                    command = command.split(";")
                    command[0] = int(command[0])
                else:
                    continue
            except redis.exceptions.TimeoutError:
                self.logger.error("Reconnecting to Redis server")
                time.sleep(1)
                self.find_active()
                continue
            except ValueError:
                self.logger.error(
                    "Failed to convert first part of the command to integer"
                )
                continue
            except Exception as e:
                self.logger.error("Listening Thread died:\n{}".format(e))
                self.log_remote("Listening Thread died: {}".format(e), now)
                time.sleep(1)
                self.find_active()
                continue

            self.logger.info("command received {}".format(command))
            if command[0] == Command.REBOOT:
                self.logger.info("Reboot command received")
                self.log_remote("Reboot command received", now)
                self.bbb.reboot()

            elif command[0] == Command.SET_HOSTNAME and len(command) == 2:
                new_hostname = command[1]
                self.bbb.update_hostname(new_hostname)
                # Updates variable names
                self.logger.info("Hostname changed to " + new_hostname)
                self.log_remote("Hostname changed to {}".format(new_hostname), now)
                self.listening = False

            elif command[0] == Command.SET_IP:
                ip_type = command[1]
                # Verifies if IP is to be set manually
                if ip_type == "manual" and len(command) == 5:
                    new_ip = command[2]
                    new_mask = command[3]
                    new_gateway = command[4]
                    self.bbb.update_ip_address(ip_type, new_ip, new_mask, new_gateway)
                    # Updates variable names
                    info = "IP manually changed to {}, netmask {}, gateway {}".format(
                        new_ip, new_mask, new_gateway
                    )
                    self.logger.info(info)
                    self.log_remote(info, now)
                    self.listening = False

                # Verifies if IP is DHCP
                elif ip_type == "dhcp":
                    self.bbb.update_ip_address(ip_type)
                    # Updates variable names
                    time.sleep(1)
                    self.logger.info("IP changed to DHCP")
                    self.log_remote("IP changed to DHCP", now)
                    self.listening = False

            elif command[0] == Command.SET_NAMESERVERS and len(command) == 3:
                nameserver_1 = command[1]
                nameserver_2 = command[2]
                self.logger.info(
                    "Nameservers changed: {}, {}".format(nameserver_1, nameserver_2)
                )
                self.log_remote(
                    "Nameservers changed: {}, {}".format(nameserver_1, nameserver_2),
                    now,
                )
                self.bbb.update_nameservers(nameserver_1, nameserver_2)

            elif command[0] == Command.STOP_SERVICE and len(command) == 2:
                service_name = command[1]
                if service_name == "bbbread":
                    self.logger.warning("Stopping BBBread")
                self.logger.info("{} service stopped".format(service_name))
                self.log_remote("{} service stopped".format(service_name), now)
                subprocess.check_output(["systemctl", "stop", service_name])

            elif command[0] == Command.RESTART_SERVICE and len(command) == 2:
                service_name = command[1]
                if service_name == "bbbread":
                    self.logger.warning("Restarting BBBread")
                self.logger.info("{} service restarted".format(service_name))
                self.log_remote("{} service restarted".format(service_name), now)
                subprocess.check_output(["systemctl", "restart", service_name])

    def log_remote(self, message, date):
        try:
            self.remote_db.hset(self.logs_name, date, message)
        except Exception as e:
            self.logger.error("Failed to send remote log information: {}".format(e))

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
            if self.remote_db.keys(old_hashname + ":Logs"):
                self.remote_db.rename(old_hashname + ":Logs", self.hashname + ":Logs")

            self.logger.info(
                "old ip: {}, new ip: {}, old hostname: {}, new hostname: {}".format(
                    self.bbb_ip, new_ip, self.bbb_hostname, new_hostname
                )
            )
            self.remote_db.hmset(old_hashname, old_info)
            self.listening = True
        # Updates remote hash
        if log:
            self.logger.info("updating remote db")

        self.remote_db.hmset(self.hashname, info)
        self.bbb_ip, self.bbb_hostname = (new_ip, new_hostname)
        self.logs_name = "BBB:{}:{}:Logs".format(self.bbb_ip, self.bbb_hostname)


if __name__ == "__main__":
    sys.exit()
