import serial

SERIAL_PORT = "COM5"

def get_port():
    return serial.Serial(port=SERIAL_PORT, baudrate=9600, timeout=1, parity=serial.PARITY_EVEN, stopbits=1)