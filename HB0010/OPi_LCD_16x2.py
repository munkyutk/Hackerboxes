#---------------------------------------------
# Orange Pi LCD Tester
# 
# From	: lcd_16x2.py (16x2 LCD Test Script)
# By	: Matt Hawkins
# Date	: 06/04/2015
# WWW	: http://www.raspberrypi-spy.co.uk/
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#--------------------------------------------

# The wiring for the LCD is as follows:
# 1  : GND
# 2  : 5V
# 3  : Contrast (0-5V)*
# 4  : RS (Register Select)
# 5  : R/W (Read/Write)  	-> Ground this pin
# 6  : Enable or Strobe
# 7  : Data Bit 0		-> NOT USED
# 8  : Data Bit 1		-> NOT USED
# 9  : Data Bit 2		-> NOT USED
# 10 : Data Bit 3		-> NOT USED
# 11 : Data Bit 4
# 12 : Data Bit 5
# 13 : Data Bit 6
# 14 : Data Bit 7
# 15 : LCD Backlight +5V**
# 16 : LCD Backlight GND

#import
from pyA20.gpio import gpio
from pyA20.gpio import port
from time import sleep

# Define GPIO to LCD mapping
LCD_RS = port.PA19
LCD_E  = port.PA7
LCD_D4 = port.PA8
LCD_D5 = port.PA9
LCD_D6 = port.PA10
LCD_D7 = port.PA20

# Define some device contants
LCD_WIDTH = 16		# Maximm characters per line
LCD_CHR = True
LCD_CMD = False

LCD_LINE_1 = 0x80 	# LCD RAM address for the 1st line
LCD_LINE_2 = 0xC0	# LCD RAM address for the 2nd line

# Timing constants
E_PULSE = 0.0005
E_DELAY = 0.0005

def main():
	try:
	# Main program block
		gpio.init();
		gpio.setcfg(LCD_E, gpio.OUTPUT)	# E
		gpio.setcfg(LCD_RS, gpio.OUTPUT) # RS
		gpio.setcfg(LCD_D4, gpio.OUTPUT) # D84
		gpio.setcfg(LCD_D5, gpio.OUTPUT) # D85
		gpio.setcfg(LCD_D6, gpio.OUTPUT) # D86
		gpio.setcfg(LCD_D7, gpio.OUTPUT) # D87
	
		# Initialize display
		lcd_init()

		while True:
			# send text
			lcd_string("Hackerboxes.com", LCD_LINE_1)
			lcd_string("hack the planet", LCD_LINE_2)
	
			sleep(2)
	
			# send text
			lcd_string("Hackerboxes.com", LCD_LINE_1)
			lcd_string("HACK THE PLANET", LCD_LINE_2)
	
			sleep(2)
	except KeyboardInterrupt:
		lcd_string("Goodbye!", LCD_LINE_1)
		print "Goodbye!"
	


def lcd_init():
	# Initialize display
	lcd_byte(0x33, LCD_CMD) # 110011 Initialize
	lcd_byte(0x32, LCD_CMD) # 110010 Initialize
	lcd_byte(0x06, LCD_CMD) # 000110 Cursor move direction
	lcd_byte(0x0C, LCD_CMD) # 001100 Display On, Cursor Off, Blink Off
	lcd_byte(0x28, LCD_CMD) # 101000 Data length, number of lines, font size
	lcd_byte(0x01, LCD_CMD) # 000001 Clear display
	sleep(E_DELAY)

def lcd_byte(bits, mode):
	# Send byte to data pins
	# bits = data
	# mode = True for character
	#        False for command

	gpio.output(LCD_RS, mode)

	# high bits
	gpio.output(LCD_D4, False)
	gpio.output(LCD_D5, False)
	gpio.output(LCD_D6, False)
	gpio.output(LCD_D7, False)

	if bits&0x10==0x10:
		gpio.output(LCD_D4, True)
	if bits&0x20==0x20:
		gpio.output(LCD_D5, True)
	if bits&0x40==0x40:
		gpio.output(LCD_D6, True)
	if bits&0x80==0x80:
		gpio.output(LCD_D7, True)

	# Toggle 'Enable' pin
	lcd_toggle_enable()

	# Low bits
	gpio.output(LCD_D4, False)
	gpio.output(LCD_D5, False)
	gpio.output(LCD_D6, False)
	gpio.output(LCD_D7, False)

	if bits&0x01==0x01:
		gpio.output(LCD_D4, True)
	if bits&0x02==0x02:
		gpio.output(LCD_D5, True)
	if bits&0x04==0x04:
		gpio.output(LCD_D6, True)
	if bits&0x08==0x08:
		gpio.output(LCD_D7, True)

	# Toggle 'Enable' pin
	lcd_toggle_enable()

def lcd_toggle_enable():
	# toggle enable
	sleep(E_DELAY)
	gpio.output(LCD_E, True)
	sleep(E_PULSE)
	gpio.output(LCD_E, False)
	sleep(E_DELAY)

def lcd_string(message, line):
	# send string to display
	message = message.ljust(LCD_WIDTH," ")

	lcd_byte(line, LCD_CMD)

	for i in range(LCD_WIDTH):
		lcd_byte(ord(message[i]),LCD_CHR)

if __name__ == '__main__':
	main()
