import logging
from logging import handlers
import socket
import pickle
import struct

class SimpleSocketHandler(logging.Handler):
    def __init__(self, host, port):
        logging.Handler.__init__(self)
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.host, self.port))
        self._setup_and_test()

    def _setup_and_test(self):
        logger = logging.getLogger('example_logger')
        logger.setLevel(logging.DEBUG)

        #socket_handler = SimpleSocketHandler('localhost', 9090)
        logger.addHandler(self)

        logger.info('This is a test log message sent to the server')
        logger.error('This is an error message sent to the server')

    def emit(self, record):
        try:
            data = self.makePickle(record)
            self.sock.sendall(data)
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            self.handleError(record)

    def makePickle(self, record):
        data = pickle.dumps(record.__dict__)
        length = struct.pack('>L', len(data))
        return length + data

    def close(self):
        self.sock.close()
        logging.Handler.close(self)


# Example usage
if __name__ == "__main__":
    socket_handler = SimpleSocketHandler('localhost', 9090)
    # logger = logging.getLogger('example_logger')
    # logger.setLevel(logging.DEBUG)
    #
    # socket_handler = SimpleSocketHandler('localhost', 9090)
    # logger.addHandler(socket_handler)
    #
    # logger.info('This is a test log message sent to the server')
    # logger.error('This is an error message sent to the server')
