import serial

class SerialComm():
    
    def __init__(self) -> None:
        self.PORT_R = "COM13"
        self.PORT_L = "COM5"

        self.baudrate = 9600

    @property
    def get_port(self):
        try:
            R = serial.Serial(port=self.PORT_R, baudrate=self.baudrate, timeout=1, parity=serial.PARITY_EVEN, stopbits=1)
        except:
            R = None

        try:
            L = serial.Serial(port=self.PORT_L, baudrate=self.baudrate, timeout=1, parity=serial.PARITY_EVEN, stopbits=1)
        except:
            L = None
        return R,L