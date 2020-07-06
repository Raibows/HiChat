import socket
import errno
import sys
import time
import threading
from queue import Queue
from tools import *



class TCPClient():
    def __init__(self, messages:Queue, server_addr=('127.0.0.1', 5000), HEADER_LEN=10):
        self.messages = messages
        self.server_addr = server_addr
        self.HEADER_LEN = HEADER_LEN
        self.stop_signal = False
        self.password = None
        self.username = None

    def connect_to_server(self):
        try:
            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client.connect(self.server_addr)
            self.client.setblocking(False)
        except:
            return False

    def register(self, username, password):
        if not self.connect_to_server(): return False
        data = self.encode_message('None', 'register', password, str(time.time()), username)
        self.client.send(data)
        while True:
            try:
                res = receive_data(self.client)
                if res: break
            except:
                continue
        return eval(res)

    def login(self, username, password):
        if not self.connect_to_server(): return False
        data = self.encode_message('None', 'login', password, str(time.time()), username)
        self.client.send(data)
        while True:
            try:
                res = receive_data(self.client)
                if res: break
            except:
                continue
        res = eval(res)
        if res:
            self.username = username
            self.password = password
            return True
        else: return False

    def encode_message(self, receiver, msg_type, message, timestamp, username=None):
        if username is None: username = self.username
        if msg_type == 'pic':
            message = open(message, 'r').read()
        data = encode_header(username) + username.encode('utf-8') + encode_header(receiver) + \
            receiver.encode('utf-8') + encode_header(msg_type) + msg_type.encode('utf-8') + \
            encode_header(message) + message.encode('utf-8') + encode_header(timestamp) + timestamp.encode('utf-8')
        return data


    def receive_msg(self):
        time.sleep(3)
        while True and not self.stop_signal:
            try:
                while True:
                    sender_header = self.client.recv(self.HEADER_LEN).decode('utf-8')
                    if not len(sender_header):
                        print("Connection closed by the Server")
                        sys.exit()
                    sender = self.client.recv(int(sender_header.strip())).decode('utf-8')
                    receiver = receive_data(self.client)
                    msg_type = receive_data(self.client)
                    msg = receive_data(self.client)
                    timestamp = receive_data(self.client)
                    if msg_type == 'text':
                        print(standard_output(sender, msg, timestamp))

            except IOError as e:
                if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
                    print('Reading error', str(e))
                    sys.exit()
                continue

            except Exception as e:
                print("General error", e)
                sys.exit()


    def send_msg(self):
        while True and not self.stop_signal:
            if self.messages.empty(): continue
            msg = self.messages.get()
            receiver = msg[0]
            msg = msg[1]
            if msg and len(msg) > 0:
                timestamp = str(time.time())
                print(standard_output(self.username, msg, timestamp))
                data = self.encode_message(receiver, 'text', msg, timestamp)
                self.client.send(data)


    def run(self):
        send_thread = threading.Thread(target=self.send_msg)
        send_thread.start()
        recv_thread = threading.Thread(target=self.receive_msg)
        recv_thread.start()







if __name__ == '__main__':
    pass
