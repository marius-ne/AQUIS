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
    def getStatus(self) -> int:
        """
        Sends the getStatus command.
        
        Returns
        -----
        status : 2 STDBY_RC, 3 STDBY_XOSC, 4 FS, 5 RX, 6 TX
        """
        byte = spilib.transceive(self.spi,self.csPin,self.busyPin,GET_STATUS,1)
        raw = struct.unpack(">B",byte)[0]

        return raw & 0x70 # isolate bits 6:4

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
        timeout : timeout (seconds). between 0 (off) and 262  for continous (only RX)
        """
        self.setStandby(0)
        timeoutBytes = int(timeout / (15.625 * (10**-6)))
        if value == 0 :
            spilib.send(self.spi,self.csPin,self.busyPin,SET_RX,[])
        elif value == 1:
            # first setting PaConfig
            pass

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

        power = 0x16 + level # lowest value that both power levels have
        bytes = [power,0x01]
        spilib.send(self.spi,self.csPin,self.busyPin,SET_TX_PARAMS,bytes)
    
    # page 82
    def setRf(self,value: int):
        """
        Sets the radio frequency. 
        
        Parameters
        -----
        value : frequency in kiloHertz
        """
        # scaling input to LSB
        rf = int(((2 ** 25) / FXTAL) * (value*1000))
        # moving along, trimming beyond 8 bits                            
        bytes = [((rf >> (8 * (3-i))) & 0xFF) for i in range(4)]
        
        spilib.send(self.spi,self.csPin,self.busyPin,SET_RF,bytes)

    # page 82
    def setType(self,value: int):
        """
        Sets the packet type of the radio.
        
        Parameters
        -----
        value : 0 GFSK, 1 LoRa
        """
        # packet type can only be changed from STDBY_RC
        self.setStandby(0)

        spilib.send(self.spi,self.csPin,self.busyPin,SET_PACKET_TYPE,[value])

    


