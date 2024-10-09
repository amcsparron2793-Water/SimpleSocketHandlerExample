"""
SimpleSocketHandlerExample.py

Client Side:

SimpleSocketHandler: A custom logging handler that inherits from logging.Handler. It
creates a socket connection to the given host and port. Logging: Adds the socket handler to the logger and sends log
messages to the remote server using the logger.info() and logger.error() methods.

Server Side:

LogReceiver: A simple
server that binds to the specified host and port, listens for incoming connections, and receives log messages. It
unpacks the message, unpickles it, and then uses logging to handle the log record.

This setup will allow you to send
and receive log messages over a network using sockets. Make sure to have both the client and server running
simultaneously to see the log messages being transmitted and received."""

import subprocess


def run_example():
    s_handler_process = subprocess.Popen(["python", "SocketHandler.py"])
    log_receiver_process = subprocess.Popen(["python", "LogReceiver.py"])
    s_handler_process.wait()
    log_receiver_process.wait()


if __name__ == '__main__':
    run_example()



