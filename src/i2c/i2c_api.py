import struct

def get_bits(number,*args):
    """
    returns state of bit
    """
    res = []
    for pos in args:
        if (number & (1 << pos)) > 0:
            res.append((number & (1 << pos)) // (number & (1 << pos)))
        else:
            res.append(0)
    return res if len(res) > 1 else res[0]

def set_bits(number,dct):
    """
    needs dict with bit positions and desired values

    error catching through checking with get_bits() that
    query makes sense, else gets ignored
    """
    for pos,val in dct.items():
        if val and get_bits(number,pos) == 0:
            number = number + 2**pos
        elif not val and get_bits(number,pos) > 0:
            number = number - 2**pos
    return number

def byte_write(i2c,address,register,subject):
    initial = bytearray(1)
    i2c.writeto(address,bytes([register]))
    i2c.readfrom_into(address,initial)
     

    i2c.writeto(address,bytes([register,subject]))
     

    changed = bytearray(1)
    i2c.writeto(address,bytes([register]))
    i2c.readfrom_into(address,changed)
     

    print(f'{hex(register)} prev: {initial[0]:08b}\n{hex(register)} now:  {changed[0]:08b}\n')

def byte_read(i2c,address,*args,len_array):
    """
    len_array is the size of the expected return from the register
    if multiple registers are provided each of them reads up to len_array
    """
    state = bytearray(len_array * len(args)) #len_array for each register if multiple registers
    for ix,reg in enumerate(args):
        i2c.writeto(address,bytes([reg]))

        #state gets sliced, each register has its place
        i2c.readfrom_into(address,state,start=len_array*ix,end=(len_array*ix)+len_array)
     
    return state
    
def byte_change(i2c,address,register,value,*args):
    original_byte = byte_read(i2c,address,register,len_array=1)
    original = struct.unpack('>B',original_byte)[0]
     
    
    base_byte = value << min(args)
    if value > 0:
        dct = {}
        for bit in args:
            dct[bit] = get_bits(base_byte,bit)
    else:
        dct = {bit:0 for bit in args}
       
    new_byte = set_bits(original,dct)
    
    for bit in args:
        if get_bits(new_byte,bit) != get_bits(base_byte,bit):
            print(base_byte,new_byte,value,args)
            raise ValueError('conversion did not work')
    byte_write(i2c,address,register,new_byte)
