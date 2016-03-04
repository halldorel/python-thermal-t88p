import serial
import math
import time

from PIL import Image

# Bytes used in commands
ESC = 0x1B
AT = 0x40
LF = 0xA
GS = 0x1D
B = 0x42
EXCL = 0x21
STAR = 0x2A
SLASH = 0x2F

# Commands
c = {}
c["RESET"] = [ESC, AT]
c["PRINT_BUFFER"] = [GS, SLASH]
c["PRINT_AND_FEED"] = [LF]
c["PRINT_AND_FEED_N"] = [ESC, 0x64]
c["SELECT_CHAR_SIZE"] = [GS, EXCL]
c["SELECT_BIT_IMAGE_MODE"] = [ESC, STAR]
c["DEFINE_IMAGE"] = [GS, STAR]
c["PRINT_IMAGE"] = [GS, SLASH]
c["INVERT"] = [GS, B]
c["CUT"] = [ESC, b'i']
c["SET_LINE_SPACING"] = [ESC, 0x33]

class Printer:
    ser = None
    def connect(self, portname='/dev/tty.usbmodemfa121', baudrate=9600):
        ser = serial.Serial(portname, baudrate=baudrate, bytesize=serial.EIGHTBITS, dsrdtr=True)
        self.ser = ser
        
        print(ser)
        return self.ser
    
    def sendBytes(self, bytes):
        self.ser.write(bytes)
        
    def sendCommand(self, commandName, n=None):
        if n == None:
            self.sendBytes(c[commandName])
        elif type(n) == list:
            print("Type is list")
            print(c[commandName] + n)
            
            self.sendBytes(c[commandName] + n)
        else:
            self.sendBytes(c[commandName] + [n])
    
    def println(self, string, feedlines=1):
        self.sendBytes(string)
        if feedlines > 1:
            self.sendCommand("PRINT_AND_FEED_N", n=feedlines)
        else:
            self.sendCommand("PRINT_AND_FEED")
    
    def setFontSize(self, vsize=1, hsize=1):
        size = vsize-1 + (hsize-1 << 4)
        self.sendCommand("SELECT_CHAR_SIZE", n=size)
        
    def setLineSpacing(self, lineSpacing=1):
        self.sendCommand("SET_LINE_SPACING", lineSpacing)
        
    def cut(self):
        self.sendCommand("CUT", [])
    
    def printImageBuffer(self, image_buffer, width, height, m=0, nL=255, nH=3):
        # m = 33 Hard-selecting 24-dot double-density mode.
        # nL = 255 Over entire paper width
        # nH = 1 One line at a time
        d = (nL + nH * 256) * 3
        self.sendCommand("SELECT_BIT_IMAGE_MODE", [m, width, height])
        
        x = int(math.ceil(width / 8))
        y = int(math.ceil(height / 8))
        
        time.sleep(0.1)
        self.sendCommand("DEFINE_IMAGE")
        self.sendBytes(image_buffer)
        time.sleep(0.1)
        self.sendCommand("PRINT_IMAGE", 0)
        
    def invert(self, on):
        if on:
            self.sendCommand("INVERT", 0xFF)
        else: 
            self.sendCommand("INVERT", 0x00)
        
    
    def printImage(self, image, width, height):
        return 0
        
    def reset(self):
        self.sendCommand("RESET")
        

def getbytes(bits):
    done = False
    while not done:
        byte = 0
        for _ in range(0, 8):
            try:
                bit = next(bits)
            except StopIteration:
                bit = 0
                done = True
            byte = (byte << 1) | bit
        yield byte

if __name__ == "__main__":
    printer = Printer()
    printer.connect(baudrate=9600)
            
    time.sleep(1)
    printer.reset()
    
    # Print string
    def test_printing_a_string():
        print("Printing a string")
        printer.println("Printing a string.")
    
    # Print and feed 3 lines
    def test_printing_and_feeding_three_lines():
        printer.println("Printing and feeding 3 lines", feedlines=3)
    
    # Font size scaled vertically by 2 and horizontally by 3
    def test_scaling_font():
        printer.setFontSize(2, 3)
        printer.println("Font size changed")
        printer.setFontSize()
        
    def test_invert():
        printer.invert(True)
        printer.println("Blessadur i beinni")
        printer.invert(False)
        printer.println("Invert off")
        
    def test_set_line_spacing():
        printer.setLineSpacing(0)
        printer.println("Blessadur")
        printer.println("Chilladur")
        printer.println("Blessadur")
        printer.println("Chilladur")
            
    time.sleep(1)
    printer.reset()    
    
    
    # test_set_line_spacing()
    # test_printing_a_string()
    # test_printing_and_feeding_three_lines()
    # test_scaling_font()
    
    # nH *256 dots
    # + nL sem er rest
    
    w = 256
    h = 24
    
    for i in range(0, h/8):
        for j in range(0, w):
            continue
    
    printer.setLineSpacing(0)
    
    time.sleep(1)
    
    
    from PIL import Image
    
    img = Image.open("hildur-2.bmp")
    pixels = img.load()
    
    def getVerticalImageByte(pixels, row):
        image_bytes = []
        for j in range(0, 256):
            bitstring = ""
            for i in range(0 + row*8, 8*row +8):
                bitstring += str(pixels[j, i])
            
            image_bytes.append(int(bitstring, 2))
        return image_bytes


    # COOL PATTERN:

    # for z in range(0, 1):
    #     printer.sendCommand("SELECT_BIT_IMAGE_MODE", [0, 0, 2])
    #     for v in range(0, 8):
    #         bytes_out = [int("01010101", 2) if x % 2 == 0 else int("10101010", 2) for x in range(0, 64)]
    #         print(bytes_out)
    #         printer.sendBytes(bytes_out)
    #         time.sleep(0.3)
    #         printer.sendBytes([0x00])

    
    # image_bytes = [int("01010101", 2) if x % 2 == 0 else int("10101010", 2) for x in range(0, 256)]

    for row in range(0, 16):
        printer.sendCommand("SELECT_BIT_IMAGE_MODE", [0, 0, 1])
        image_bytes = getVerticalImageByte(pixels, row)
        
        for i, byte in enumerate(image_bytes):
            print(i)
            if i%64 == 0:
                print("Will sleep now")
                time.sleep(0.3)
            printer.sendBytes([byte])
        # Send PRINT BUFFER command after sending image data
        
        printer.sendBytes([0xA])
        time.sleep(0.3)
        
    
    
    # time.sleep(1)
    # printer.sendBytes([0xFF if x % 2 == 0 else 0x00 for x in range(0, 512)])
    # time.sleep(1)
    # printer.sendBytes([0xFF if x % 2 == 0 else 0x00 for x in range(0, 512)])

    time.sleep(0.02)
    
    # printer.sendCommand("SELECT_BIT_IMAGE_MODE", [33, 0, 3])
    # printer.sendBytes([(x*17)%256 for x in range(0, 2304)])
    # time.sleep(2)
    #
    # printer.sendCommand("SELECT_BIT_IMAGE_MODE", [33, 0, 3])
    # printer.sendBytes([(x*17)%256 for x in range(0, 2304)])
    # time.sleep(2)
    #
    
    time.sleep(0.2)
    
    # #printer.sendCommand("DEFINE_IMAGE", [16, 5] + img_bytes)
    #
    # #printer.sendBytes(img_bytes)
    #
    # time.sleep(0.5)
    #
    # printer.sendCommand("PRINT_IMAGE", 0)
    #
    # time.sleep(0.5)
    #
    
    time.sleep(0.5)

