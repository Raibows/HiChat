import os
from time import ctime
import tkinter as tk
from datetime import datetime


class MessageNode():
    def __init__(self, msg_type, timestamp, msg, sender, receiver):
        self.msg_type = msg_type
        self.timestamp = timestamp
        self.msg = msg
        self.sender = sender
        self.receiver = receiver

    def get_output(self, sending):
        if self.msg_type == 'text':
            msg = try_decode(self.msg) + '\n'
            return standard_output(self.sender, self.receiver, self.timestamp, sending), msg
        elif self.msg_type == 'pic':
            return standard_output(self.sender, self.receiver, self.timestamp, sending), self.msg
        return None, None

    def __gt__(self, other):
        return self.timestamp > other.timestamp

    def __eq__(self, other):
        return self.timestamp == other.timestamp


def clone(widget):
    parent = widget.nametowidget(widget.winfo_parent())
    cls = widget.__class__

    clone = cls(parent)
    for key in widget.configure():
        clone.configure({key: widget.cget(key)})
    return clone

def file_exist(path):
    return os.path.exists(path)

def get_time()->str:
    return str(datetime.now().strftime("%H:%M:%S"))

def standard_output(sender, receiver, timestamp, sending=False):
    if isinstance(sender, bytes): username = sender.decode('utf-8')
    if isinstance(receiver, bytes): receiver = sender.decode('utf-8')
    if isinstance(timestamp, bytes): timestamp = timestamp.decode('utf-8')
    timestamp = datetime.fromtimestamp(float(timestamp))
    if sending:
        return f"{sender} >> {receiver} [{timestamp.strftime('%H:%M:%S')}]\n"
    else:
        return f"{receiver} << {sender} [{timestamp.strftime('%H:%M:%S')}]\n"

def receive_data(socket, _header_len=10, decode_flag=False)->bytes:
    try:
        header = socket.recv(_header_len)
        if not len(header): return None
        header = int(header.decode('utf-8').strip())
        data = socket.recv(header)
        if decode_flag: return data.decode('utf-8')
        else: return data
    except:
        return None


def encode_header(data, _len=10)->bytes:
    if isinstance(data, float): data = str(data)
    if isinstance(data, str): data = data.encode('utf-8')
    return f"{len(data) :< {_len}}".encode('utf-8')

def try_encode(msg):
    if isinstance(msg, bytes): return msg
    try:
        msg = msg.encode('utf-8')
    except:
        pass
    return msg

def try_decode(msg):
    if isinstance(msg, str): return msg
    try:
        msg = msg.decode('utf-8')
    except:
        pass
    return msg

if __name__ == '__main__':
    x = '123'
    print(x.encode('utf-8'))