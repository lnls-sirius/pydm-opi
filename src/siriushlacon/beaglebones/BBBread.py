import logging
import os
import time

import redis

LA_SERVER_IP = "10.0.38.46"
CA_SERVER_IP = "10.0.38.59"
LOG_PATH_SERVER = "bbbread.log"
device = "server"


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
