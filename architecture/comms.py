
def encode(data):
    enc = data.encode('utf-8')
    return enc

def decode(data):
    return data.decode('utf-8')

def transmit():
    with open('log.csv','r') as f:
        inp = f.read().strip('\n')
    with open('transmit.txt','w') as f:
        for i in inp:
            f.write(str(ord(i)))