import socket
import select
from tools import *
from queue import Queue
import threading

class User():
    def __init__(self, username, password, register_date):
        self.username = username
        self.password = password
        self.register_date = register_date

class TCPServer():
    def __init__(self, addr='127.0.0.1', port=5000, max_req=10, HEADER_LEN=10):
        self.addr = (addr, port)
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(self.addr)
        self.server.listen(max_req)
        self.HEADER_LEN = HEADER_LEN
        self.sockets_list = [self.server]
        self.users = {}
        self.clients_id = {}
        self.clients_sk = {}
        self.messages = Queue()

    def receive_msg(self, client:socket.socket):
        sender = receive_data(client)
        receiver = receive_data(client)
        msg_type = receive_data(client)
        msg = receive_data(client)
        timestamp = receive_data(client)
        return (msg_type, sender, receiver, msg, timestamp)

    def encode_msg(self, msg:tuple)->bytes:
        msg_type = msg[0].encode('utf-8')
        sender = msg[1].encode('utf-8')
        receiver = msg[2].encode('utf-8')
        message = msg[3].encode('utf-8')
        timestamp = msg[4].encode('utf-8')
        data = encode_header(sender) + sender + encode_header(receiver) + receiver + \
        encode_header(msg_type) + msg_type + encode_header(message) + message + encode_header(timestamp) + timestamp
        return data


    def broadcast(self):
        while True:
            if not self.messages.empty():
                data = self.messages.get()
                if data[2] not in self.users: continue # receiver not exits
                if data[2] not in self.clients_id: # receiver offline
                    self.messages.put(data)
                    continue
                self.clients_id[data[2]].send(self.encode_msg(data))

    def handle_register(self, client_sk:socket.socket, data):
        if data[1] in self.users:
            res = 'False'
            print(f"{get_time()} New Register failed from {client_sk.getsockname()} username {data[1]}")
        else:
            self.users[data[1]] = User(data[1], data[3], data[4])
            self.clients_id[data[1]] = client_sk
            self.clients_sk[client_sk] = data[1]
            self.sockets_list.append(client_sk)
            print(f"{get_time()} New Register success from {client_sk.getsockname()} username {data[1]}")
            res = 'True'
        res = encode_header(res) + res.encode('utf-8')
        client_sk.send(res)

    def handle_login(self, client_sk:socket.socket, data):
        res = 'False'
        if data[1] not in self.users:
            res = 'False'
            print(f"{get_time()} Login failed from {client_sk.getsockname()} username {data[1]}")
        elif data[3] == self.users[data[1]].password:
            res = 'True'
            self.clients_id[data[1]] = client_sk
            self.clients_sk[client_sk] = data[1]
            self.sockets_list.append(client_sk)
            print(f"{get_time()} Login success from {client_sk.getsockname()} username {data[1]}")
        res = encode_header(res) + res.encode('utf-8')
        client_sk.send(res)


    def listening(self):
        print(f"{get_time()} Server {self.addr[0]}:{self.addr[1]} is running!")
        while True:
            read_sockets, _, exception_sockets = select.select(self.sockets_list, [], self.sockets_list)
            for sk in read_sockets:
                if sk == self.server:
                    client_sk, client_addr = self.server.accept()
                    data = self.receive_msg(client_sk)
                    if data[0] == 'register':
                        self.handle_register(client_sk, data)
                    elif data[0] == 'login':
                       self.handle_login(client_sk, data)
                else:
                    msg = self.receive_msg(sk)
                    if None in msg:
                        print(f"{get_time()} Closed connection from {sk.getsockname()}")
                        self.sockets_list.remove(sk)
                        del self.clients_id[self.clients_sk[sk]]
                        del self.clients_sk[sk]
                    else:
                        print(f"{get_time()} Received {msg}")
                        self.messages.put(msg)

            for sk in exception_sockets:
                self.sockets_list.remove(sk)
                del self.clients_id[self.clients_sk[sk]]
                del self.clients_sk[sk]

    def run(self):
        listen_thread = threading.Thread(target=self.listening)
        listen_thread.start()
        broadcast_thread = threading.Thread(target=self.broadcast)
        broadcast_thread.start()
        listen_thread.join()







if __name__ == '__main__':
    server = TCPServer()
    server.run()

