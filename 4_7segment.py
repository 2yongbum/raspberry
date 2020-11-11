#!/usr/bin/python
# Bert's code re-written for common anode LED arrays.
#blachanc: used dougie's code and added external data input in ramdisk
import RPi.GPIO as GPIO
import time
import sys
GPIO.setmode(GPIO.BCM)
#GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(7, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

#LED pin == GPIO == segment / digit
# 11     ==  24  == a
# 07     ==  12  == b
# 04     ==  19  == c
# 02     ==  21  == d
# 01     ==  23  == e
# 10     ==  22  == f
# 05     ==  15  == g
# 03     ==  11  == dp

segments = (24,12,19,21,23,22,15,11)

for segment in segments:
  GPIO.setup(segment, GPIO.OUT)
  GPIO.output(segment, 1)

# 12     ==  26  == digit 1
# 09     ==  18  == digit 2
# 08     ==  16  == digit 3
# 06     ==  13  == digit 4

digits = (26,18,16,13)
for digit in digits:
  GPIO.setup(digit, GPIO.OUT)
  GPIO.output(digit, 0)

charactere = {' ':(1,1,1,1,1,1,1),
'0':(0,0,0,0,0,0,1),
'1':(1,0,0,1,1,1,1),
'2':(0,0,1,0,0,1,0),
'3':(0,0,0,0,1,1,0),
'4':(1,0,0,1,1,0,0),
'5':(0,1,0,0,1,0,0),
'6':(0,1,0,0,0,0,0),
'7':(0,0,0,1,1,1,1),
'8':(0,0,0,0,0,0,0),
'9':(0,0,0,0,1,0,0)}
counter=100000

##############################
# use a file on ramdisk to get the data to be displayed
# bash commands passed in terminal:
# echo "1235" > /tmp/display.dat
###############################
def get_data_to_display():
    txt=open("/tmp/display.dat")
    new_string = str(txt.readline())
    txt.close()
    new_string=new_string.rstrip()
	#
	# buf with 0 if less than 4 char
	#
    new_string= str(new_string).rjust(4,"0")
	#
	# limit to 4 chars
	#
    new_string= new_string[0:4]
    return new_string
###########
# main loop
###########
try:
  while True:
    #
	# First we only update the data to display each x loops
	#
    counter +=1
    if (counter > 50):
       counter = 0
       new_string = get_data_to_display()
# for debug only       print  new_string
       data_to_display = new_string

    for digit in range(4):
      for loop in range(0,7):
        GPIO.output(segments[loop], charactere[data_to_display[digit]][loop])
      GPIO.output(digits[digit], 1)
      time.sleep(0.001)
      GPIO.output(digits[digit], 0)

except KeyboardInterrupt:
  GPIO.cleanup()
