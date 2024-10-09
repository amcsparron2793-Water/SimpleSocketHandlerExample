import socket
import struct
import pickle
import logging


class LogReceiver:
    """
    Class representing a log receiver that listens for log records over a TCP connection.

    Attributes:
        host (str): The host address to bind the socket to. Default is 'localhost'.
        port (int): The port number to bind the socket to. Default is 9090.

    Methods:
        __init__: Initializes the LogReceiver with the specified host and port, creating a socket and starting to listen.
        start: Starts accepting connections and handling log records over the connection.
        handle_log_record: Handles a received log record by logging the record using the record's name.
    """
    def __init__(self, host='localhost', port=9090):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.host, self.port))
        self.sock.listen(1)

    def start(self):
        """
        Handles incoming log records over a socket connection.

        Accepts incoming connections and processes log records
        until a keyboard interrupt occurs or an exception is raised.

        Logs any errors that occur during the process.
        """
        connection, address = self.sock.accept()
        print(f'Connected by {address}')
        while True:
            try:
                length_data = connection.recv(4)
                if not length_data:
                    break
                length = struct.unpack('>L', length_data)[0]
                log_data = connection.recv(length)
                record = logging.makeLogRecord(pickle.loads(log_data))
                self.handle_log_record(record)
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f'Error: {e}')
                break

    def handle_log_record(self, record):
        """
        Handles a log record by retrieving a logger instance based on the record's name
        and then passing the record to the logger's handle method.
        """
        logger = logging.getLogger(record.name)
        logger.handle(record)


if __name__ == "__main__":
    receiver = LogReceiver()
    print('Starting log receiver...')
    receiver.start()
