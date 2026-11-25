import serial


def print_ticket(queue_no: int, port: str = "/dev/ttyUSB0") -> None:
    with serial.Serial(port, 9600, timeout=2) as s:
        s.write(b"\x1b@BRIGHTWELL\n\nYour number: %d\n\n\x1dV\x00" % queue_no)
