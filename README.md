Python EPSON-TM88P printer library
==================================

This library is intended to interface with the EPSON-TM88P line of thermal printers. It was written using http://www.pwks.de/driver/PDF/t88i2.pdf as a reference for the serial protocol. 

Install deps
------------
	pip install pyserial

Testing
-------
	from printer import Printer
	printer.connect('/dev/tty.name-of-serial-port', baudrate=9600)
	printer.println("Hello, world!")

This is still a work in progress. As my T88P only has a serial port, I built a simple logic level shifter from a MAX232 IC, and am using an Arduino Uno as a USB to Serial interface. That is done by shorting the RESET pin to Ground on the Arduino, and it shows up on my Mac as `/dev/tty.usbmodemfa121`.
