Changes to Online detector
# http://xanthium.in/Cross-Platform-serial-communication-using-Python-and-PySerial
# https://stackoverflow.com/questions/2438848/set-serial-port-pin-high-using-python
# http://pyserial.readthedocs.io/en/latest/pyserial_api.html
# python -m serial.tools.list_ports will print a list of available ports
# pySerial small console based terminal program called serial.tools.miniterm:
# It ca be started with python -m serial.tools.miniterm <port_name>

TOP:
import serial           # import the module
import fieldtrip


# connect to ports
ft = fieldtrip.connect.buffer
# ser = serial.Serial(**bco_port**, timeout=None, baudrate=115000, xonxoff=False, rtscts=False, dsrdtr=False)
ser = serial.Serial('COM24') # open COM24 for sending triggers
ser.baudrate = 9600 # set Baud rate to 9600
ser.bytesize = 8    # Number of data bits = 8
ser.parity   = 'N'  # No parity
ser.stopbits = 1    # Number of Stop bits = 1



handle_detect()
  # Write character 'A' to serial port
  data = bytearray(b'A')
  No = ser.write(data)

  ser.close()         # Close the Com port

  # OR!!! Controlling RTS and DTR Pins in Python (2 pints from the 9)
  # Serial ports send 8 bits of a byte in serie, so 1 at a time (as opposed
  # to 8 bits at the same time in a parallel port)
  # RTS: Request to Send and DTR: Data Terminal Ready (were used for modem control)
  # RTS and DTR pins can be controlled by using setRTS() and setDTR()
  # functions available in the pySerial module. The functions can be
  # used to SET and CLEAR the RTS and DTR pins. (add delay after using)
  ser.SetRTS(0) ser.SetRTS(1)
  ser.setDTR(0) ser.SetDTR(1)

  # how to read?
  ser.rts works as getter? dsrdtr, rtscts, work as getters




  #--------------------------------------------
# Stimulation computer
import serial                    # import pySerial module

# ser = serial.Serial(**bco_port**, timeout=None, baudrate=115000, xonxoff=False, rtscts=False, dsrdtr=False)
ser = serial.Serial('COM24') # open the COM Port
ser.timeout= None            # set timeout
ser.baudrate = 9600          # set Baud rate
ser.bytesize = 8             # Number of data bits = 8
ser.parity   = 'N'           # No parity
ser.stopbits = 1             # Number of Stop bits = 1

While True:
    bytesToRead = ser.inWaiting()  Wait and read data
    data = ser.read(bytesToRead)
    print data # print the received data
    ser.close() # Close the COM Port
