import serial

SERIAL_PORT_R = "COM13"
SERIAL_PORT_L = "COM5"

def get_port() -> tuple[serial.Serial,serial.Serial]:
    try:
        R = serial.Serial(port=SERIAL_PORT_R, baudrate=9600, timeout=1, parity=serial.PARITY_EVEN, stopbits=1)
    except:
        R = None

    try:
        L = serial.Serial(port=SERIAL_PORT_L, baudrate=9600, timeout=1, parity=serial.PARITY_EVEN, stopbits=1)
    except:
        L = None
    return (R,L)