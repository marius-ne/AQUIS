# def byteWrite(spi,csPin,register: int,subject: int,printRes: bool=True):
#     """
#     Method to write new byte to spi register.
    
#     Parameters
#     -----
#     spi : spi object from busio.SPI
#     csPin : control slave pin from board.D##
#     register : address of register to be written to
#     subject : number representation (endian-ness depends on slave) of new byte to be written
#     """
#     csPin = False

#     # reading initial register state
#     initial = bytearray(1)
#     spi.write(bytes([register]))
#     spi.readinto(initial)
    
#     # writing new state
#     spi.write(bytes([register,subject]))

#     # checking new state
#     changed = bytearray(1)
#     spi.write(bytes([register]))
#     spi.readinto(changed)

#     csPin = True
#     if printRes:
#         print(f'byteWrite() on register {hex(register)}\nreg. prev: {initial[0]:08b} reg. now: {changed[0]:08b}\n')

# def byteRead(spi,csPin: int,register: int,nReg: int=1) -> bytearray:
#     """
#     Method to read current state of the given registers. 
    
#     Parameters
#     -----
#     spi : spi object from busio.SPI
#     csPin : control slave pin from board.D##
#     register : register to be read
#     nReg : keyword argument to determine length of reading from each register, defaults to 1. 
#                 If > 1 it must be checked that the device allows consecutive reading.
#     """
#     # nReg for each register if multiple registers
#     state = bytearray(nReg) 
#     csPin = False
    
#     spi.writeto(bytes([register]))

#     for i in range(nReg):  
#         #state gets sliced, each register has its place
#         spi.readinto(state,start=nReg*i,end=(nReg*i)+nReg)

#     csPin = True
#     return state
    
# def byteChange(spi,csPin: int,register: int,values: dict):
#     """
#     Method to read register and only change bits provided, leaving the rest as is.
    
#     Parameters
#     -----
#     spi : spi object from busio.SPI
#     csPin : control slave pin from board.D##
#     register : register to be changed
#     values : dictionary of new bits(values) with positions(keys)
#     """
#     original = byteRead(spi,csPin,register)[0]

#     for ix, i in values.items():
#         new = original &  ~(1 << ix) # clearing the bit
#         new |= i << ix # setting the bit

#     byteWrite(spi,csPin,register,new)

def send(spi,csPin,busyPin,cmd: int,params: list):
    """
    Method to send commands to an SPI slave.
    
    Parameters
    -----
    spi : spi object from busio.SPI
    csPin : control slave pin from board.D##
    cmd : opcode of command
    params : optional bytes (as int) to send after opcode
    """
    # wait until BUSY goes low
    while busyPin.value:
        pass

    csPin = False

    spi.writeto(bytes([cmd] + params))

    csPin = True

def transceive(spi,csPin,busyPin,cmd: int,len: int) -> bytearray:
    """
    Method to receive data by an SPI slave after sending a command.
    
    Parameters
    -----
    spi : spi object from busio.SPI
    csPin : control slave pin from board.D##
    cmd : opcode of command
    len : number of bytes to receive

    Returns
    -----
    arr : bytearray of length len with received bytes
    """
    # wait until BUSY goes low
    while busyPin.value:
        pass

    arr = bytearray(len)
    csPin = False

    spi.writeto(bytes([cmd]))
    spi.readinto(arr)

    csPin = True
    return arr