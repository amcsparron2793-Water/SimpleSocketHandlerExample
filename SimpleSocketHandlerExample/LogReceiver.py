import socket
import struct
import pickle
import logging


class LogReceiver:
    def __init__(self, host='localhost', port=9090):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.host, self.port))
        self.sock.listen(1)

    def start(self):
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
        logger = logging.getLogger(record.name)
        logger.handle(record)


if __name__ == "__main__":
    receiver = LogReceiver()
    print('Starting log receiver...')
    receiver.start()
