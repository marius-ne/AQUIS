import spilib
import struct
import time

# important numbers
FXTAL = 32 * (10 ** 6) # crystal frequency

# registers
RNG0 = 0x0819
RNG1 = 0x081A
RNG2 = 0x081B
RNG3 = 0x081C
SYNC_L = 0x06C0

# commands (opcode)
NOP = 0x00
GET_STATUS = 0xC0
WRITE_REG = 0x0D
READ_REG = 0x1D
SET_SLEEP = 0x84
SET_STANDBY = 0x80
SET_FS = 0xC1
SET_TX = 0x83
SET_RX = 0x82
SET_RF = 0x86
SET_PACKET_TYPE = 0x8A
SET_PA_CONFIG = 0x95
SET_TX_PARAMS = 0x8E

# datasheet: https://datasheet.lcsc.com/szlcsc/2004230932_SEMTECH-SX1268IMLTRT_C244368.pdf
class DRF1268T():

    def __init__(self,spi,csPin,busyPin):
        self.spi = spi
        self.csPin = csPin
        self.busyPin = busyPin

    #page 94
    def getStatus(self) -> tuple:
        """
        Sends the getStatus command.
        
        Returns
        -----
        chipMode : 2 STDBY_RC, 3 STDBY_XOSC, 4 FS, 5 RX, 6 TX
        commandStatus : 2 Data available, 3 Cmd timeout, 4 Cmd invalid, 5 Cmd error, 6 TX success
        """
        byte = spilib.transceive(self.spi,self.csPin,self.busyPin,GET_STATUS,1)
        raw = struct.unpack(">B",byte)[0]

        return (raw & 0x70, raw & 0x0E) # isolate bits 6:4 and 3:1

    # page 65
    def setSleep(self,value: int):
        """
        Sets the operating mode of the IC.
        
        Parameters
        -----
        value : 0 cold start, 5 warm start
        """
        # sleep can only be set from STDBY_RC
        self.setStandby(0)
        
        spilib.send(self.spi,self.csPin,self.busyPin,SET_SLEEP,[value])
        time.sleep(0.05) # device needs 500us to change state

    # page 66
    def setStandby(self,value: int):
        """
        Sets the operating mode of the IC.
        
        Parameters
        -----
        value : 0 STDBY_RC (least power), 1 STDBY_XOSC
        """
        spilib.send(self.spi,self.csPin,self.busyPin,SET_STANDBY,[value])
        time.sleep(0.05) # device needs 500us to change state

    # page 66/67
    def setMode(self, value: int, timeout: int):
        """
        Sets the radio into TX / RX.
        
        Parameters
        -----
        value : 0 RX, 1 TX
        timeout : timeout (seconds). between 0 (off) and 262 for continous (only RX)
        """
        self.setStandby(0)
        
        if timeout >= 262:
            bytes = [0xFF,0xFF,0xFF]
        else:
            timeoutLSB = int(timeout / (15.625e-06))
            bytes = []
            for i in range(3):                          
                bytes.append((timeoutLSB >> (8 * (2-i))) & 0xFF) # shifting along, keeping last 8 bits

        if value == 0 :
            spilib.send(self.spi,self.csPin,self.busyPin,SET_RX,bytes)
        elif value == 1:
            spilib.send(self.spi,self.csPin,self.busyPin,SET_TX,bytes)

    # page 74
    def setTxPower(self,value: int,level: int):
        """
        Sets PA config and TX Params. Table 13-21 and 13-40 have the settings.
        Using 20us ramp time.

        Parameters
        -----
        value : 0 for low power, 1 for high power
        level : between 0 (lowest) to 217 (highest)
        """
        # first setting PaConfig, then TxParams
        # PaConfig byte sequences
        bytes = [0x00,0x03,0x00,0x01] if value == 0 else [0x04,0x07,0x00,0x01] 
        spilib.send(self.spi,self.csPin,self.busyPin,SET_PA_CONFIG,bytes) 

        # 0x16 + 0xD9 = 0xEF
        power = 0x16 + level # lowest value that both power levels have
        bytes = [power,0x01]
        spilib.send(self.spi,self.csPin,self.busyPin,SET_TX_PARAMS,bytes)
    
    # page 82
    def setRf(self,frequency: int):
        """
        Sets the radio frequency. 
        
        Parameters
        -----
        value : frequency in kiloHertz
        """
        # scaling input to LSB
        rf = int(((2 ** 25) * (frequency*1000)) / FXTAL)
        # converting to four bytes
        bytes = []
        for i in range(4):                          
            bytes.append((rf >> (8 * (3-i))) & 0xFF) # shifting along, keeping last 8 bits
        
        spilib.send(self.spi,self.csPin,self.busyPin,SET_RF,bytes)

    # page 82
    def setPacketType(self,value: int):
        """
        Sets the packet type of the radio.
        
        Parameters
        -----
        value : 0 GFSK, 1 LoRa
        """
        # packet type can only be changed from STDBY_RC
        self.setStandby(0)

        spilib.send(self.spi,self.csPin,self.busyPin,SET_PACKET_TYPE,[value])

    def setSyncWord(self,value: int=0x4151554953):
        """
        Sets the sync word before the preamble. Will only receive
        if messages start with that sync word.
        
        Parameters
        ----
        value : maximum of 8 byte sync word (default Ascii of "AQUIS")
        """
        bytes = []
        for i in range(8):     
            next = (value >> (8 * (7-i))) & 0xFF # shifting along, keeping last 8 bits             
            if next != 0:
                bytes.append(next) 
        spilib.send(self.spi,self.csPin,self.busyPin,SYNC_L,bytes)

    # page 87
    def setPacketParams(self):
        """
        Sets the packet parameters for TX and RX.
        Required before writing to the buffer.
        
        Parameters
        -----
        
        payloadLength : length of payload to transmit / max length to receive. 0 to 255
        packetType : 0 fixed size, 1 variable size
        syncWordLength : length of sync word in bytes (default 5)
        preambleLength : length of preamble in bytes (default 4)"""
        pass

