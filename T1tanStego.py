from PIL import Image
import argparse
import binascii

# Text formatting for help dialogues
example_text = '''example(s):\npython T1tanStego.py -c cyan INFILE.png OUTFILE.png\npython T1tanStego.py -v INFILE.png OUTFILE.png\npython T1tanStego.py INFILE.png OUTFILE.png -c red -f 3'''
colorHelpText = "white = red + blue + green (default)\nyellow = red + green\nmagenta = red + blue\ncyan = blue + green"
formatHelpText = "This is the direction in which Bits are replaced during encoding.\nLRTB = Left -> Right, Top -> Bottom (default)\nRLTB = Right -> Left, Top -> Bottom\nLRBT = Left -> Right, Bottom -> Top\nRLBT = Right -> Left, Bottom -> Top\nR = random! (We use SOME_ALGORITHM to randomly encode the bits throughout the picture)"

# Parser assignment for CLI positional args
parser = argparse.ArgumentParser(prog="T1tanStego", description="Encode and decode messages within PNG, JPG, etc. files using Steganography!\n"
	+ "USAGE:\npython STEGO.py INPUT_FILE OUTPUT_FILE -c COLOR_OPTIONS_(RGB) -i INPUT_FILE_WITH_MESSAGE -k OPTIONAL_KEY -d OPTIONAL_DIGEST",
                                 epilog=example_text, formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument("inputFile", type=str, help="Picture to be treated as input")
parser.add_argument("outputFile", type=str, help="The result picture that is saved as output after the program finishes")
parser.add_argument("message", nargs="+", type=str, help="The message to embed into inputFile, which creates outputFile")

# Need to finish this mutex group to read message from str or input_file
# groupMsg = parser.add_mutually_exclusive_group()
# groupMsg.add_argument("-m", action="store_true")
# groupMsg.add_argument("-M", action="store_true")

# Mutex group for quiet/verbose options (probably not needed here)
# group = parser.add_mutually_exclusive_group()
# group.add_argument("-v", "--verbose", action="store_true")
# group.add_argument("-q", "--quiet", action="store_true")

# Parser assignment for CLI optional args
parser.add_argument("-k", "--key", type=str, help="optional key to encode message")
parser.add_argument("-c", "--color", type=str, choices=["white", "red", "green", "blue", "yellow", "magenta", "cyan"], default="white", help=colorHelpText)
parser.add_argument("-f", "--format", type=str, choices=["LRTB", "RLTB", "TBLR", "TBRL", "R"], default="LRTB", help=formatHelpText)

#parse args
args = parser.parse_args()

print "Your message is: {}".format(args.message)

def doRand(args):	#needs work
	#needs work
	print "not ready" 

def doRLTB(args):	#done
	#Right-to-left, top-to-bottom:
	#X starts at max	X goes to 0
	#Y starts at 0 		Y goes to max
	
	msg=args.message
	binMsg = bin(int(binascii.hexlify(str(msg)), 16))
	print "Your message in binary is: {}".format(binMsg)

	length=len(msg)
	msgPos=0

	im = Image.open(args.inputFile)	#Can be many different formats.
	pix = im.load()
	width = im.size[0]
	height = im.size[1]

	x=width-1
	y=0

	print "Picture resolution is: {}\nPicture height is: {}\nPicture width is: {}".format(im.size, height, width)

	while y < height: 			# height
		while x >= 0:			# width
			rgb = pix[x,y]			# get RGB of pixel
			green = int(rgb[1])		# get green value
			
			if green % 2 != binMsg[msgPos]:	# mismatched bits, need to add 1 to green value
				red = int(rgb[0])		# get red value
				blue = int(rgb[2])		# get blue value
				pix[x,y] = (red,green+1,blue,255)
				msgPos += 1
			else:								# matching bits, do nothing except increment msgPos
				msgPos += 1
			x = x-1
			if msgPos == length: 	# if msg is done, move backwards 1 spot, till the pic is finished.
				msgPos-=1; 	# This will make all trailing pixels '1'
		y = y + 1
		x = width-1

	im.save(args.outputFile) 	# Save the modified picture with encrypted pixels as a new image

def doTBLR(args):	#Top-to-bottom, left-to-right
	"""
	X starts at 0		X goes to max
	Y starts at 0 		Y goes to max
	"""
	
	msg=args.message
	binMsg = bin(int(binascii.hexlify(str(msg)), 16))
	print "Your message in binary is: {}".format(binMsg)

	#bin2str
	# oldMsg = binascii.unhexlify('%x' % int(binMsg, 2))
	# print "Back to ascii: {}".format(oldMsg)

	length=len(msg)
	msgPos=0

	im = Image.open(args.inputFile)	#Can be many different formats.
	pix = im.load()
	width = im.size[0]
	height = im.size[1]

	x=0
	y=0

	print "Picture resolution is: {}\nPicture height is: {}\nPicture width is: {}".format(im.size, height, width)

	#print pix[x,y] 		 	#Get the RGBA Value of the a pixel of an image
	#pix[x,y] = (red,green+1,blue,255) 	#Set the RGBA Value of the image (tuple)
	#print pix[x,y]

	while x < width:				# width
		while y < height: 			# height
			rgb = pix[x,y]			# get RGB of pixel
			green = int(rgb[1])		# get green value
			
			#print "Checking bit: {}".format(binMsg[msgPos])
			
			if green % 2 != binMsg[msgPos]:	# mismatched bits, need to add 1 to green value
				red = int(rgb[0])		# get red value
				blue = int(rgb[2])		# get blue value
				pix[x,y] = (red,green+1,blue,255)
				msgPos += 1
			else:								# matching bits, do nothing except increment msgPos
				msgPos += 1
			y = y + 1
			if msgPos == length: # if msg is done, move backwards 1 spot, till the pic is finished.
				msgPos-=1;		 #     -This will make all trailing pixels '1' no matter what, since that's the last bit of msg
		y = 0
		x = x+1

	im.save(args.outputFile) 	# Save the modified picture with encrypted pixels as a new  	#in progress

def doTBRL(args):	#done
	"""
	X starts at max		X goes to 0
	Y starts at 0 		Y goes to max
	"""

	#binMsg = '0' + '0'.join(format(ord(x), 'b') for x in msg)
	#binMsg = bin(int.from_bytes(msg.encode(), 'big'))
	# from bin to ascii:
		# n = int('0b110100001100101011011000110110001101111', 2)
		# binascii.unhexlify('%x' % n)
	msg=args.message
	binMsg = bin(int(binascii.hexlify(str(msg)), 16))
	print "Your message in binary is: {}".format(binMsg)

	#bin2str
	# oldMsg = binascii.unhexlify('%x' % int(binMsg, 2))
	# print "Back to ascii: {}".format(oldMsg)

	length=len(msg)
	msgPos=0

	im = Image.open(args.inputFile)	#Can be many different formats.
	pix = im.load()
	width = im.size[0]
	height = im.size[1]

	x=width-1
	y=0

	print "Picture resolution is: {}\nPicture height is: {}\nPicture width is: {}".format(im.size, height, width)

	#print pix[x,y] 			#Get the RGBA Value of the a pixel of an image
	#pix[x,y] = (red,green+1,blue,255) 	#Set the RGBA Value of the image (tuple)
	#print pix[x,y]

	while x >= 0:				# width
		while y < height: 		# height
			rgb = pix[x,y]		# get RGB of pixel
			green = int(rgb[1])	# get green value
			#print "Checking bit: {}".format(binMsg[msgPos])
			if green % 2 != binMsg[msgPos]:	# mismatched bits, need to add 1 to green value
				red = int(rgb[0])		# get red value
				blue = int(rgb[2])		# get blue value
				pix[x,y] = (red,green+1,blue,255)
				msgPos += 1
			else:								# matching bits, do nothing except increment msgPos
				msgPos += 1
			y = y+1
			if msgPos == length: # if msg is done, move backwards 1 spot, till the pic is finished.
				msgPos-=1;		 #     -This will make all trailing pixels '1' no matter what, since that's the last bit of msg
		x = x - 1
		y = 0 

	im.save(args.outputFile) 	# Save the modified picture with encrypted pixels as a new  	#in progress

def doLRTB(args):	#default
	x=0
	y=0

	msg=args.message
	binMsg = bin(int(binascii.hexlify(str(msg)), 16))
	print "Your message in binary is: {}".format(binMsg)

	length=len(msg)
	msgPos=0

	im = Image.open(args.inputFile)	#Can be many different formats.
	pix = im.load()
	width = im.size[0]
	height = im.size[1]

	print "Picture resolution is: {}\nPicture height is: {}\nPicture width is: {}".format(im.size, height, width)

	# need to incorporate color choices (r,g,b,cyan,white,etc..)
	# need to add key encryption
	# need to add encode/decode flag and functionality
	while y < height: 			# height
		while x < width:		# width
			rgb = pix[x,y]			# get RGB of pixel
			green = int(rgb[1])		# get green value
			#print "Checking bit: {}".format(binMsg[msgPos])
			if green % 2 != binMsg[msgPos]:	# mismatched bits, need to add 1 to green value
				red = int(rgb[0])		# get red value
				blue = int(rgb[2])		# get blue value
				pix[x,y] = (red,green+1,blue,255)
				msgPos += 1
			else:								# matching bits, do nothing except increment msgPos
				msgPos += 1
			x = x+1
			if msgPos == length: # if msg is done, move backwards 1 spot, till the pic is finished.
				msgPos-=1;		 #     -This will make all trailing pixels '1' no matter what, since that's the last bit of msg
		y = y + 1
		x = 0

	im.save(args.outputFile) 	# Save the modified picture with encrypted pixels as a new png 	# DONE!

if args.format == "R":
	doRand(args)
elif args.format == "RLTB":
	doRLTB(args)
elif args.format == "TBLR":
	doTBLR(args)
elif args.format == "TBRL":
	doTBRL(args)
else: #default value = LRTB (standard "Western" style)
	doLRTB(args)

# 640x480 = 307200
# 8bit per byte
# 1 byte per char
# changing 1 color will result in 38400 characters (thats too many chars)

# x = [0-639]
# y = [0-399]

# Pixel formatting is (R,G,B,A) using 0-255 scale of values.

#RGB splitting notes
"""
//
rgb = pix[x,y]
red = rgb[0]
green = rgb[1]
blue = rgb[2]
//

Probable client usage command:
	python STEGO.py INPUT_FILE OUTPUT_FILE -c COLOR_OPTIONS_(RGB) -i INPUT_FILE_WITH_MESSAGE -k OPTIONAL_KEY -d OPTIONAL_DIGEST

"""
