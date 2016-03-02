import serial

# Bytes used in commands
ESC = 0x1B
AT = b'@'
LF = 0xA
GS = 0x1D
EXCL = 0x21


# Commands
c = {}
c["RESET"] = [ESC, AT]
c["PRINT_AND_FEED"] = [LF]
c["PRINT_AND_FEED_N"] = [ESC, 0x64]
c["SELECT_CHAR_SIZE"] = [GS, EXCL]

class Printer:
    ser = None
    def connect(self, portname='/dev/tty.usbmodemfa121', baudrate=9600):
        print(portname)
        ser = serial.Serial(portname)
        ser.baudrate = baudrate
        self.ser = ser
        return self.ser
    
    def sendBytes(self, bytes):
        self.ser.write(bytes)
        
    def sendCommand(self, command):
        self.sendBytes(command)
    
    def println(self, string, feedlines=1):
        self.sendBytes(string)
        if feedlines > 1:
            self.sendCommand(c["PRINT_AND_FEED_N"] + [feedlines])
        else:
            command = c["PRINT_AND_FEED"]
            self.sendCommand(c["PRINT_AND_FEED"])
    
    def setFontSize(self, vsize=1, hsize=1):
        size = vsize-1 + (hsize-1 << 4)
        self.sendCommand(c["SELECT_CHAR_SIZE"] + [size])
    
    def printImage(self, image, width, height):
        return 0
        
    def reset(self):
        sendCommand(c.RESET)
        
        
if __name__ == "__main__":
    printer = Printer()
    printer.connect()
    
    # Print string
    printer.println("Printing a string.")
    
    # Print and feed 3 lines
    printer.println("Printing and feeding 3 lines", feedlines=3)
    
