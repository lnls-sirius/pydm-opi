import pickle
import struct
from common.entity.entities import Command
import ipaddress

def get_valid_address(ip):
    return str(ip) if type(ip) == ipaddress.ip_address else str(ipaddress.ip_address(ip))

class NetUtils():
    @staticmethod
    def send_failure(connection, error_message):
        """
        Sends a failure message to a given connection socket.
        :param connection: the connection to be used to send the integer.
        :param error_message: a message explaining the failure.
        """
        NetUtils.send_command(connection, Command.FAILURE)
        NetUtils.send_object(connection, error_message)

    @staticmethod
    def send_command(connection, command):
        """
        Sends a command through the connection.
        :param connection: the connection to be used to send the integer.
        :param command: A 4-byte integer representing a command.
        """
        connection.send(struct.pack("!i", command))

    @staticmethod
    def recv_command(connection):
        """
        Receives a single 4-byte integer.
        :param connection: the connection to be used to receive the integer.
        :return: the integer representing a command.
        """
        return struct.unpack("!i", connection.recv(4))[0]

    @staticmethod
    def send_data(connection, data):
        """
        Sends bytes through the connection. First, its sends how many bytes the data is composed of.
        :param connection: the connection to be used to send the object.
        :param data: the data to bem sent.
        """
        connection.send(struct.pack("!i", len(data)))
        connection.send(data)

    @staticmethod
    def recv_data(connection):
        """
        Receives bytes from a connection. First, its reads how many bytes were sent.
        :param connection: the connection to be used to receive the object.
        :return: the received data.
        """
        data_size = struct.unpack("!i", connection.recv(4))[0]
        return connection.recv(data_size)

    @staticmethod
    def recv_object(connection):
        """
        Receives an object and de-serializes it.
        :param connection: the connection to be used to receive the object.
        :return: de-serialized object.
        """
        return pickle.loads(NetUtils.recv_data(connection))

    @staticmethod
    def send_object(connection, obj=None):
        """
        Serialize the object with pickle and sends it through the connection.
        :param connection: the connection that will be used to send the object.
        :param obj: the object to be sent.
        """
        NetUtils.send_data(connection, pickle.dumps(obj))

    @staticmethod
    def checksum(data_str):
        if type(data_str) != bytes:
            packet = data_str.strip().encode('utf-8') 
            
        else:
            packet = data_str 
        total = 0
        # Add up 16-bit words
        num_words = len(packet) // 2
        for chunk in struct.unpack("!%sH" % num_words, packet[0:num_words * 2]):
            total += chunk

        # Add any left over byte
        if len(packet) % 2:
            packet[-1]
            for packet_str in list(str(packet[-1])):
                for packet_char in packet_str: 
                    total += ord(packet_char) << 8

        # Fold 32-bits into 16-bits
        total = (total >> 16) + (total & 0xffff)
        total += total >> 16
        return ~total + 0x10000 & 0xffff

    @staticmethod
    def compare_checksum(expected_chk, payload):
        """
        Compares the received message's and the object checksum fields. This method must be updated
        as the data format sent by the bbb is modified.
        Message content: {chk} | {payload}
        :param data: received packet to be verified.
        :return: Array containing the payload.
        :raise ValueError: checksum fields do not match.
        """
        if not type(payload) == dict:
            raise TypeError("Incorrect payload type. Expected python dictionary but received {}.".format(type(payload)))
        
        payload_str = str(payload)

        res = NetUtils.checksum(payload_str)

        if int(res) == expected_chk:
            return payload

        raise ValueError("Computed and received checksum fields do not match. Computed, received  {} != {}".format(int(res), expected_chk))
