from pyA20.gpio import gpio
from pyA20.gpio import port
from time import sleep

gpio.init()

MATRIX = [ [1,2,3,'A'],
	   [4,5,6,'B'],
	   [7,8,9,'C'],
	   ['*',0,'#','D'] ]

ROW = [1, 6, 11, 12]
COL = [3, 0, 14, 13]

for j in range(4):
	gpio.setcfg(COL[j], gpio.OUTPUT)
	gpio.output(COL[j], 1)

for i in range(4):
	gpio.setcfg(ROW[i], gpio.INPUT)
	gpio.pullup(ROW[i], gpio.PULLUP)

try:
	while(True):
		for j in range(4):
			gpio.output(COL[j], 0)

			for i in range(4):
				if gpio.input(ROW[i]) == 0:
					print MATRIX[i][j]
					while(gpio.input(ROW[i])==0):
						pass

			gpio.output(COL[j], 1)
except KeyboardInterrupt:
	print "Goodbye"
