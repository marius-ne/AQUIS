def byteWrite(i2c,address: int,register: int,subject: int,printRes: bool=True):
    """
    Method to write new byte to I2C register.
    
    Parameters
    -----
    i2c : i2c object from busio.I2C
    address : WHO_AM_I address of slave
    register : address of register to be written to
    subject : number representation (endian-ness depends on slave) of new byte to be written
    """
    # reading initial register state
    initial = bytearray(1)
    i2c.writeto(address,bytes([register]))
    i2c.readfrom_into(address,initial)
     
    
    i2c.writeto(address,bytes([register,subject]))

    # checking new state
    changed = bytearray(1)
    i2c.writeto(address,bytes([register]))
    i2c.readfrom_into(address,changed)

    if printRes:
        print(f'byteWrite() on register {hex(register)}\nreg. prev: {initial[0]:08b} reg. now: {changed[0]:08b}\n')

def byteRead(i2c,address: int,register: int,nReg: int=1) -> bytearray:
    """
    Method to read current state of the given registers. 
    
    Parameters
    -----
    i2c : i2c object from busio.I2C
    address : WHO_AM_I address of slave
    register : register to be read
    nReg : keyword argument to determine length of reading from each register, defaults to 1. 
                If > 1 it must be checked that the device allows consecutive reading.
    """
    # nReg for each register if multiple registers
    state = bytearray(nReg)
    i2c.writeto(address,bytes([register]))

    for i in range(nReg):  
        #state gets sliced, each register has its place
        i2c.readfrom_into(address,state,start=nReg*i,end=(nReg*i)+nReg)
    return state
    
def byteChange(i2c,address: int,register: int,values: dict):
    """
    Method to read register and only change bits provided, leaving the rest as is.
    
    Parameters
    -----
    i2c : i2c object from busio.I2C
    address : WHO_AM_I address of slave
    register : register to be changed
    values : dictionary of new bits(values) with positions(keys)
    """
    original = byteRead(i2c,address,register)[0]

    for ix, i in values.items():
        new = original &  ~(1 << ix) # clearing the bit
        new |= i << ix # setting the bit

    byteWrite(i2c,address,register,new)