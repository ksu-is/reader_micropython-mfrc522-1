import mfrc522
from os import uname

#I added the following code so that you can assign the tag a specific name or code before writing on it

import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import time

ledb= 3
ledr= 5
buz= 7

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(ledb,GPIO.OUT)
GPIO.setup(ledr,GPIO.OUT)
GPIO.setup(buz,GPIO.OUT)
reader = SimpleMFRC522()

try:
        GPIO.output(ledb,1)
        GPIO.output(ledr,0)
        GPIO.output(buz,0)
        reg_no = raw_input('Registration Number:')
        GPIO.output(ledb,1)
        GPIO.output(ledr,1)
        GPIO.output(buz,0)
        print("Now place your tag to write")
        reader.write(reg_no)
        print("Written")
        GPIO.output(ledb,0)
        GPIO.output(ledr,0)
        GPIO.output(buz,1)
        time.sleep(0.5)
        GPIO.output(ledb,0)
        GPIO.output(ledr,0)
        GPIO.output(buz,0)

finally:
        GPIO.cleanup()

def do_write():

	if uname()[0] == 'WiPy':
		rdr = mfrc522.MFRC522("GP14", "GP16", "GP15", "GP22", "GP17")
	elif uname()[0] == 'esp8266':
		rdr = mfrc522.MFRC522(0, 2, 4, 5, 14)
	else:
		raise RuntimeError("Unsupported platform")

	print("")
	print("Place card before reader to write address 0x08")
	print("")

	try:
		while True:

			(stat, tag_type) = rdr.request(rdr.REQIDL)

			if stat == rdr.OK:

				(stat, raw_uid) = rdr.anticoll()

				if stat == rdr.OK:
					print("New card detected")
					print("  - tag type: 0x%02x" % tag_type)
					print("  - uid	 : 0x%02x%02x%02x%02x" % (raw_uid[0], raw_uid[1], raw_uid[2], raw_uid[3]))
					print("")

					if rdr.select_tag(raw_uid) == rdr.OK:

						key = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]

						if rdr.auth(rdr.AUTHENT1A, 8, key, raw_uid) == rdr.OK:
							stat = rdr.write(8, b"\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f")
							rdr.stop_crypto1()
							if stat == rdr.OK:
								print("Data written to card")
							else:
								print("Failed to write data to card")
						else:
							print("Authentication error")
					else:
						print("Failed to select tag")

	except KeyboardInterrupt:
		print("Bye")
