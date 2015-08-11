import RPi.GPIO as GPIO
from Adafruit_7Segment import SevenSegment
#from Adafruit_LEDBackpack import LEDBackpack
import time as time
import math as math

def quarterInsert():
	global coins
	coins = coins + 25
	updateDisplay()


def dimeInsert():
	global coins
	coins = coins + 10
	updateDisplay()


def nickelInsert():
	global coins
	coins = coins + 5
	updateDisplay()

def select():
	global keypressed
	global selection
	global coins
	third = 0
	second = 0
	while "loop" == "loop":
		key()
		if keypressed == 10:
			GPIO.output(RESETled, 1)
			selection = 0
		elif third == 0 and keypressed < 3:
			selection = keypressed * 100
			third = 1
		elif second == 0:
			selection = selection + keypressed * 10
			second = 1
		elif first == 0 and keypressed < 8:
			selection = selection + keypressed
			break
		updateDisplay()
	coins = coins - 25
	updateDisplay()
	return selection


def key():
	global keypressed
	keypressed = 11
	while keypressed == 11:
		GPIO.output(GRY, 1)
		if GPIO.input(YEL) == 1:
			keypressed = 8
		if GPIO.input(ORN) == 1:
			keypressed = 9
		if GPIO.input(BRN) == 1:
			keypressed = 10
		GPIO.output(GRY, 0)

		GPIO.output(PUR, 1)
		if GPIO.input(YEL) == 1:
			keypressed = 5
		if GPIO.input(ORN) == 1:
			keypressed = 6
		if GPIO.input(BRN) == 1:
			keypressed = 7
		GPIO.output(PUR, 0)

		GPIO.output(BLU, 1)
		if GPIO.input(YEL) == 1:
			keypressed = 3
		if GPIO.input(ORN) == 1:
			keypressed = 4
		GPIO.output(BLU, 0)

		GPIO.output(GRN, 1)
		if GPIO.input(YEL) == 1:
			keypressed = 0
		if GPIO.input(ORN) == 1:
			keypressed = 1
		if GPIO.input(BRN) == 1:
			keypressed = 2
		GPIO.output(GRN, 0)


def play(position):
	"Loads and plays record "
	# Homes wheel
	GPIO.output(SPIN, 1)
	time.sleep(0.1)
	GPIO.wait_for_edge(HOME, GPIO.RISING)
	if get_digit(selection, 3) == 2:
		GPIO.wait_for_edge(HOME, GPIO.RISING)
	# Starts countiong
	for x in xrange(0, position):
		GPIO.wait_for_edge(OPTO, GPIO.RISING)
	# Loads record
	GPIO.output(SPIN, 0)
	GPIO.output(LOAD, 1)
	time.sleep(1)
	GPIO.output(LOAD, 0)

def get_digit(num, position):
	place = 10 ** position
	return int(num / place) % 10

def updateDisplay():
	leftScreen.writeDigit(get_digit(int(math.floor(coins/25)),0),0)
	leftScreen.writeDigit(get_digit(int(math.floor(coins/25)),1),1)
	if get_digit(selection, 3) != 0:
		rightScreen.writeDigit(0, get_digit(selection, 1))
	else:
		rightScreen.writeDigitRaw(0, 0x0040)

	if get_digit(selection, 2) != 
	0:
		rightScreen.writeDigit(1, get_digit(selection, 2))
	else:
		rightScreen.writeDigitRaw(1, 0x0040)

	if get_digit(selection, 1) != 0:
		rightScreen.writeDigit(3, get_digit(selection, 3))
	else:
		rightScreen.writeDigitRaw(3, 0x0040)
#--------------------------------------------------------------------
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
keypressed = 11
coins = 0
selection = 0
songs = {100: 1, 101: 2, 110: 8, 200: 1}
PUR = 35
BLU = 32
GRN = 36
YEL = 38
ORN = 40
BRN = 37
GRY = 33
QUARTER = 21
HALF = 29
SPIN = 18
NICKEL = 31
LOAD = 22
OPTO = 7
RESETled = 12
ADDled = 8
SELECTIONled = 19
PLAYINGled = 10
DIME = 23
HOME = 11
AB = 13
# Keyboard
GPIO.setup(GRY, GPIO.OUT)
GPIO.setup(PUR, GPIO.OUT)
GPIO.setup(BLU, GPIO.OUT)
GPIO.setup(GRN, GPIO.OUT)
GPIO.setup(YEL, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(ORN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(BRN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
# Coin Switch
GPIO.setup(QUARTER, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.add_event_detect(QUARTER, GPIO.RISING, callback=quarterInsert)
GPIO.setup(DIME, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.add_event_detect(DIME, GPIO.RISING, callback=dimeInsert)
GPIO.setup(NICKEL, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.add_event_detect(NICKEL, GPIO.RISING, callback=nickelInsert)
# Record Loading
GPIO.setup(SPIN, GPIO.OUT)
GPIO.setup(LOAD, GPIO.OUT)
GPIO.setup(HOME, GPIO.IN)
GPIO.setup(OPTO, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
# LEDs
GPIO.setup(RESETled, GPIO.OUT)
GPIO.setup(ADDled, GPIO.OUT)
GPIO.setup(PLAYINGled, GPIO.OUT)
GPIO.setup(SELECTIONled, GPIO.OUT)
# Seven Segments
leftScreen = SevenSegment(address=0x70)
rightScreen = SevenSegment(address=0x71)
#LEDleftScreen = LEDBackpack(address=0x70)
#LEDrightScreen = LEDBackpack(address=0x71)
updateDisplay()

#----------------------------------------------------

while "loop" == "loop":
	while coins <= 25:
		GPIO.output(ADDled, 1)
		time.sleep(.5)
	print("25c inserted")
	GPIO.output(ADDled, 0)
	GPIO.output(SELECTIONled, 1)
	play(songs[select()])
	GPIO.output(SELECTIONled, 0)
	GPIO.output(PLAYINGled, 1)
