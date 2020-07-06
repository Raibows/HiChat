import os
from time import ctime
from datetime import datetime

def get_time()->str:
    return str(datetime.now().strftime("%H:%M:%S"))

def standard_output(username, msg, timestamp):
    timestamp = datetime.fromtimestamp(float(timestamp))
    return f">>{username}    {timestamp.strftime('%H:%M:%S')} \n{msg}"

def receive_data(socket, _header_len=10)->str:
    try:
        header = socket.recv(_header_len)
        if not len(header): return None
        header = int(header.decode('utf-8').strip())
        data = socket.recv(header)
        return data.decode('utf-8')
    except:
        return None


def encode_header(data, _len=10)->bytes:
    if isinstance(data, str): data = data.encode('utf-8')
    return f"{len(data) :< {_len}}".encode('utf-8')

def try_encode(msg):
    try:
        msg = msg.encode('utf-8')
    except:
        pass
    return msg

def try_decode(msg):
    try:
        msg = msg.decode('utf-8')
    except:
        pass
    return msg

if __name__ == '__main__':
    x = '123'
    print(x.encode('utf-8'))