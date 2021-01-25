import struct

def get_bits(number,*args):
    """
    method to get bit-states of binary representation of a number
    
    :param number: number to read bits from
    :param *args: desired bit positions, from right to left, starting at 0
    :type number: int
    :type *args: int
    
    :returns: list of the bit-states in order of the positions provided
    :rtype: list if len(args) > 1 else int
    """
    res = []
    for pos in args:
        if (number & (1 << pos)) > 0:
            res.append((number & (1 << pos)) // (number & (1 << pos)))
        elif (number & (1 << pos)) == 0:
            res.append(0)
        else:
            raise ValueError('Somehow got negative bit value!')
    return res if len(res) > 1 else res[0]

def set_bits(number,dct):
    """
    method to return number with bits in binary representation changed

    :param number: number to set bits to
    :param dct: bits as keys with desired states (0 or 1) as values
    :type number: int
    :type dct: dict
    
    :returns: number with bits changed
    :rtype: int
    """
    for pos,val in dct.items():
        if val and get_bits(number,pos) == 0:
            number = number + 2**pos
        elif not val and get_bits(number,pos) > 0:
            number = number - 2**pos
        elif val < 0:
            raise ValueError('Cannot set bits to negative value!')
    return number

def byte_write(i2c,address,register,subject,print_change=True):
    """
    method to write new byte to i2c register
    
    :param i2c: i2c object from busio.I2C
    :param address: WHO_AM_I address of slave
    :param register: address of register to be written to
    :param subject: number representation (endian-ness depends on slave) of new byte to be written
    
    :type i2c: busio.I2C object
    :type address: int
    :type register: int
    :type subject: int
    
    :returns: nothing
    :rtype: None
    """
    initial = bytearray(1)
    i2c.writeto(address,bytes([register]))
    i2c.readfrom_into(address,initial)
     
    i2c.writeto(address,bytes([register,subject]))

    changed = bytearray(1)
    i2c.writeto(address,bytes([register]))
    i2c.readfrom_into(address,changed)

    if print_change:
        print(f'byte_write() on register {hex(register)}\nreg. prev: {initial[0]:08b} reg. now: {changed[0]:08b}\n')
    return None

def byte_read(i2c,address,*args,len_array=1):
    """
    method to read current state of the given registers
    
    :param i2c: i2c object from busio.I2C
    :param address: WHO_AM_I address of slave
    :param *args: register to be read
    :param len_array: keyword argument to determine length of reading from each register, defaults to 1
    
    :type i2c: busio.I2C object
    :type address: int
    :type *args: int
    :type len_array: int
    
    :returns: bytearray with length: len(args) * len_array
    :rtype: bytearray object
    """
    state = bytearray(len_array * len(args)) #len_array for each register if multiple registers
    for ix,reg in enumerate(args):
        i2c.writeto(address,bytes([reg]))

        #state gets sliced, each register has its place
        i2c.readfrom_into(address,state,start=len_array*ix,end=(len_array*ix)+len_array)
    return state
    
def byte_change(i2c,address,register,value,*args):
    """
    method to read register and only change bits provided, leaving the rest as is
    
    :param i2c: i2c object from busio.I2C
    :param address: WHO_AM_I address of slave
    :param register: register to be changed
    :param value: number to indicate the new value. e.g. changing 000 to 110 requires value 6. assumes no trailing zeros, position in byte determined by :param *args:
    :param *args: bits that will be affected by the change. e.g. changing 000100 to 001010 requires bits 3,2,1 (indexed from right to left, starting at 0)
    
    :type i2c: busio.I2C object
    :type address: int
    :type register: int
    :type value: int
    :type *args: int
    
    :returns: nothing
    :rtype: None
    """
    original_byte = byte_read(i2c,address,register,len_array=1)
    original = struct.unpack('>B',original_byte)[0]
    
    if min(args) < 0:
        print(f'value: {value}, args: {args}, register: {register}')
        raise ValueError('Negative value not allowed!\nBits in a byte indexed 0-7 from right to left.')
        
    elif value > 0 and len(args) != value.bit_length():
        print(f'value: {value}, args: {args}, register: {register}')
        raise ValueError('Please provide all / only those bits that will change with given value!\ne.g. value 5 in bit position 3 (00101000) requires bits 3,4,5 - indexed 0-7 from right to left.')
        
    for bit in args:
        if bit != min(args) and bit - 1 not in args:
            print(f'value: {value}, args: {args}, register: {register}')
            raise ValueError('Please provide only the changing bits in consecutive order.\nUndefined behaviour will occur otherwise!')
      
    #shifting value into place
    base_byte = value << min(args)
    if value > 0:
        dct = {}
        for bit in args:
            dct[bit] = get_bits(base_byte,bit) #getting changed bits with given value
    else:
        dct = {bit:0 for bit in args} #if value is 0 multiple bits may be set to 0
       
    new_byte = set_bits(original,dct)
    byte_write(i2c,address,register,new_byte)
    return None